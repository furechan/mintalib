"""Generic indicator model.

One runtime ``Indicator`` class is specialized along independent input and
output type axes.  The four public names are static aliases rather than
distinct runtime classes.
"""

from __future__ import annotations

import inspect
from operator import itemgetter, methodcaller
from types import MappingProxyType
from typing import Any, Callable, Generic, ParamSpec, TypeAlias, TypeVar, cast, overload

import numpy as np
import pandas as pd
from pandas.api.typing import Expression

from ..utils import format_partial


SeriesSource: TypeAlias = pd.Series | pd.DataFrame
Prices: TypeAlias = pd.DataFrame

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")
NextOutputT = TypeVar("NextOutputT")
IndicatorT = TypeVar("IndicatorT", bound="Indicator[Any, Any]")
P = ParamSpec("P")


class _Composition:
    def __init__(self, left: Callable[[Any], Any], right: Callable[[Any], Any]):
        self.left = left
        self.right = right

    def __call__(self, data: Any) -> Any:
        return self.right(self.left(data))


def _make_expression(func: Callable[[pd.DataFrame], pd.Series], repr_str: str) -> Expression:
    return Expression(func, repr_str)  # pyright: ignore[reportCallIssue]


class Indicator(Generic[InputT, OutputT]):
    """Typed shell around a runtime indicator callable."""

    def __init__(
        self,
        func: Callable[[InputT], OutputT],
        repr_str: str,
        output_names: tuple[str, ...] = (),
        *,
        series_input: bool = False,
    ):
        self._func = func
        self._repr = repr_str
        self.output_names = output_names
        self._series_input = series_input

    def __call__(self, data: InputT) -> OutputT:
        return self._func(data)

    def __repr__(self) -> str:
        return self._repr

    def __or__(
        self: Indicator[InputT, pd.Series],
        other: Indicator[SeriesSource, NextOutputT],
    ) -> Indicator[InputT, NextOutputT]:
        if self.output_names:
            raise TypeError("only a series-output indicator can be composed")
        if not isinstance(other, Indicator) or not other._series_input:
            raise TypeError("an indicator can only be followed by a series-input indicator")
        return Indicator(
            _Composition(self, other),
            f"{self!r} | {other!r}",
            other.output_names,
            series_input=self._series_input,
        )

    def alias(
        self: Indicator[InputT, pd.Series],
        name: str,
    ) -> Indicator[InputT, pd.Series]:
        return Indicator(
            _Composition(self, methodcaller("rename", name)),
            f"{self!r}.alias({name!r})",
            series_input=self._series_input,
        )

    def __getitem__(
        self: Indicator[InputT, pd.DataFrame],
        item: str,
    ) -> Indicator[InputT, pd.Series]:
        if item not in self.output_names:
            names = ", ".join(self.output_names)
            raise KeyError(f"{item!r}: unknown output column. Valid: {names}.")
        return Indicator(
            _Composition(self, itemgetter(item)),
            f"{self!r}[{item!r}]",
            series_input=self._series_input,
        )

    @overload
    def as_expr(self: Indicator[InputT, pd.Series]) -> Expression: ...

    @overload
    def as_expr(self: Indicator[InputT, pd.DataFrame], item: str) -> Expression: ...

    def as_expr(self, item: str | None = None) -> Expression:
        if item is None:
            if self.output_names:
                raise TypeError("item is required for a multi-output indicator")
            return _make_expression(cast(Any, self), repr(self))
        if not self.output_names:
            raise TypeError("item is only valid for a multi-output indicator")
        frame = cast(Indicator[Any, pd.DataFrame], self)
        selected = frame[item]
        return _make_expression(cast(Any, selected), repr(selected))


class IndicatorBundle:
    """Named collection of indicators evaluated against the same prices.

    Keyword argument names become result column names. Positional indicators
    must return a named Series or a DataFrame with named columns.
    """

    def __init__(self, *args: Callable[[Prices], Any], **kwargs: Callable[[Prices], Any]):
        self.args = args
        self.kwargs = kwargs

    def items(self):
        for arg in self.args:
            yield None, arg
        yield from self.kwargs.items()

    def __repr__(self) -> str:
        params = ", ".join(f"{name}={item!r}" if name else repr(item) for name, item in self.items())
        return f"{type(self).__name__}({params})"

    def calc(self, prices: Prices, *, merge: bool = False) -> pd.DataFrame:
        """Calculate the bundled columns, optionally merging them with the input."""
        if not isinstance(prices, pd.DataFrame):
            raise TypeError(
                f"IndicatorBundle only accepts pandas DataFrames, got {type(prices).__name__}. "
                "For polars, use mintalib.expressions.ExprBundle."
            )

        columns: dict[Any, Any] = {}
        for name, indicator in self.items():
            result = indicator(prices)
            if isinstance(result, pd.DataFrame):
                columns.update(result)
            elif name is not None:
                columns[name] = result
            elif isinstance(result, pd.Series) and result.name is not None:
                columns[result.name] = result
            else:
                raise ValueError(f"unexpected result type {type(result).__name__} in positional arguments")

        result = pd.DataFrame(columns, index=prices.index)
        if not merge:
            return result

        merged = prices.copy()
        merged[result.columns] = result
        return merged

    def __call__(self, prices: Prices, *, merge: bool = False) -> pd.DataFrame:
        return self.calc(prices, merge=merge)


SeriesToSeries: TypeAlias = Indicator[SeriesSource, pd.Series]
SeriesToFrame: TypeAlias = Indicator[SeriesSource, pd.DataFrame]
PricesToSeries: TypeAlias = Indicator[Prices, pd.Series]
PricesToFrame: TypeAlias = Indicator[Prices, pd.DataFrame]


def func_name(func: Callable[..., Any]) -> str:
    return getattr(func, "__name__", type(func).__name__)


def _wrap_result(
    result: Any,
    source: pd.Series | pd.DataFrame,
) -> pd.Series | pd.DataFrame:
    asdict = getattr(result, "_asdict", None)
    if asdict is not None:
        result = asdict()

    index = source.index if isinstance(source, (pd.Series, pd.DataFrame)) else None
    if isinstance(result, dict):
        return pd.DataFrame(result, index=index)
    if isinstance(result, np.ndarray):
        return pd.Series(result, index=index)
    if isinstance(result, (pd.Series, pd.DataFrame)):
        return result
    raise TypeError(f"unexpected kernel result {type(result).__name__}")


def _inputs(calc_func: Callable[..., Any]) -> tuple[str, ...]:
    metadata = getattr(calc_func, "metadata", {})
    inputs = metadata.get("inputs")
    if not inputs:
        raise ValueError(f"missing inputs metadata for {func_name(calc_func)!r}")
    return tuple(inputs)


class _BoundKernel:
    """A kernel with constructor parameters and input dispatch bound."""

    def __init__(
        self,
        calc_func: Callable[..., Any],
        params: dict[str, Any],
        *,
        input_kind: str,
        item: str | None,
        inputs: tuple[str, ...],
    ):
        self.calc_func = calc_func
        self.params = MappingProxyType(params)
        self.input_kind = input_kind
        self.item = item
        self.inputs = inputs

    def __call__(self, data: SeriesSource) -> pd.Series | pd.DataFrame:
        if not isinstance(data, (pd.DataFrame, pd.Series)):
            raise TypeError(
                "indicators only accept pandas DataFrames or Series; "
                f"got {type(data).__name__}. For polars, use mintalib.expressions."
            )

        if self.input_kind == "series":
            source = data[self.item or "close"] if isinstance(data, pd.DataFrame) else data
            result = self.calc_func(source, **self.params)
        else:
            if not isinstance(data, pd.DataFrame):
                raise TypeError(
                    f"{func_name(self.calc_func)} requires a pandas DataFrame with price columns; "
                    f"got {type(data).__name__}."
                )
            result = self.calc_func(
                *(data[name] for name in self.inputs),
                **self.params,
            )

        return _wrap_result(result, data)


def _kernel_dispatch(calc_func: Callable[..., Any]) -> tuple[str, tuple[str, ...]]:
    parameters = tuple(inspect.signature(calc_func).parameters)
    first = parameters[0]
    if first == "series":
        return "series", ()

    inputs = _inputs(calc_func)
    if parameters[: len(inputs)] == inputs:
        return "columns", inputs
    raise ValueError(f"kernel inputs do not match metadata for {func_name(calc_func)!r}")


def _update_wrapper(
    wrapper: Callable[..., Any],
    func: Callable[..., Any],
    calc_func: Callable[..., Any],
    signature: inspect.Signature,
) -> None:
    setattr(wrapper, "__name__", func_name(func))
    setattr(wrapper, "__qualname__", getattr(func, "__qualname__", func_name(func)))
    setattr(wrapper, "__module__", getattr(func, "__module__", None))
    setattr(wrapper, "__doc__", getattr(calc_func, "__doc__", None))
    setattr(wrapper, "metadata", getattr(calc_func, "metadata", {}))
    setattr(wrapper, "__signature__", signature)


def wrap_indicator(
    calc_func: Callable[..., Any],
) -> Callable[[Callable[P, IndicatorT]], Callable[P, IndicatorT]]:
    """Decorate an annotated indicator factory while preserving its return type."""

    input_kind, inputs = _kernel_dispatch(calc_func)
    metadata = getattr(calc_func, "metadata", {})
    output_names = tuple(metadata.get("output_names", ()))

    def decorator(func: Callable[P, IndicatorT]) -> Callable[P, IndicatorT]:
        signature = inspect.signature(func)

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> IndicatorT:
            binding = signature.bind(*args, **kwargs)
            binding.apply_defaults()
            display_params = dict(binding.arguments)
            params = dict(display_params)
            item = params.pop("item", None)
            runtime = _BoundKernel(
                calc_func,
                params,
                input_kind=input_kind,
                item=item,
                inputs=inputs,
            )
            repr_str = format_partial(func, display_params, name=func_name(func))
            return cast(
                IndicatorT,
                Indicator(
                    cast(Any, runtime),
                    repr_str,
                    output_names,
                    series_input=input_kind == "series",
                ),
            )

        _update_wrapper(wrapper, func, calc_func, signature)
        return wrapper

    return decorator


__all__ = [
    "Indicator",
    "IndicatorBundle",
    "Prices",
    "PricesToFrame",
    "PricesToSeries",
    "SeriesSource",
    "SeriesToFrame",
    "SeriesToSeries",
    "wrap_indicator",
]
