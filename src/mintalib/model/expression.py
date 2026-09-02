"""Expressions Model"""

import inspect
from collections.abc import Iterable

import polars as pl

from typing import TypeAlias, ParamSpec, Callable, Any, Protocol, overload
from polars.datatypes import Struct, Float64


IntoExpr: TypeAlias = pl.Expr | str
"""Type alias for Polars expressions accepted as inputs."""

CLOSE = pl.col("close")
"""Expression for the close price column."""

OHLC = pl.struct(["open", "high", "low", "close"])
"""Expression for open, high, low, and close columns as a struct."""

P = ParamSpec("P")


class ExprBundle(tuple[pl.Expr, ...]):
    """Named collection of expressions destined for one frame context."""

    def __new__(cls, *args: IntoExpr, **kwargs: IntoExpr) -> "ExprBundle":
        items = tuple(get_series_expr(arg) for arg in args)
        items += tuple(get_series_expr(arg).alias(name) for name, arg in kwargs.items())
        return super().__new__(cls, items)

    def over(self, by: IntoExpr | Iterable[IntoExpr]) -> "ExprBundle":
        """Apply the same window partition to every expression."""
        return ExprBundle(*(expr.over(by) for expr in self))

    def as_struct(self, name: str | None = None) -> pl.Expr:
        """Pack the expressions into one struct expression."""
        struct = pl.struct(self)
        return struct.alias(name) if name is not None else struct

    def __add__(self, other: Iterable[pl.Expr]) -> "ExprBundle":
        if isinstance(other, str) or not isinstance(other, Iterable):
            return NotImplemented
        return ExprBundle(*self, *other)

    def __radd__(self, other: Iterable[pl.Expr]) -> "ExprBundle":
        if isinstance(other, str) or not isinstance(other, Iterable):
            return NotImplemented
        return ExprBundle(*other, *self)


class ExprFactory(Protocol[P]):
    """
    Call signature of wrapped expression factories.

    Wrapped factories accept an optional leading polars expression as `src`,
    so they compose with `Expr.pipe` as in `EMA(20).pipe(ROC, 1)`.
    """

    @overload
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> pl.Expr: ...
    @overload
    def __call__(self, src: pl.Expr, /, *args: P.args, **kwargs: P.kwargs) -> pl.Expr: ...



def get_series_expr(src):
    if isinstance(src, str):
        return pl.col(src)
    
    if isinstance(src, pl.Expr):
        return src

    raise ValueError("src must be a string or a Polars expression.")


def get_input_expr(src, name: str):
    if isinstance(src, str):
        return pl.col(src).alias(name)

    if isinstance(src, pl.Expr):
        return src.alias(name)

    raise ValueError(f"{name} must be a string or a Polars expression.")


def _get_inputs(calc_func) -> tuple[str, ...]:
    metadata = getattr(calc_func, "metadata", {})
    declared_inputs = metadata.get("inputs")

    if not declared_inputs:
        raise ValueError(f"Missing inputs metadata for {calc_func.__name__!r}")

    return tuple(declared_inputs)


def _get_output_type(calc_func):
    metadata = getattr(calc_func, "metadata", {})
    output_names = metadata.get("output_names", ())
    return Struct({name: Float64 for name in output_names}) if output_names else Float64


def _wrap_batch_output(output):
    asdict = getattr(output, "_asdict", None)
    if asdict is not None:
        return pl.DataFrame(asdict(), nan_to_null=True).to_struct()

    return pl.Series(output, nan_to_null=True)


def _update_wrapper(wrapper, func, calc_func, signature):
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    wrapper.__module__ = func.__module__
    wrapper.__doc__ = calc_func.__doc__
    setattr(wrapper, "metadata", getattr(calc_func, "metadata", {}))
    setattr(wrapper, "__signature__", signature)
    return wrapper


def wrap_series_expression(calc_func) -> Callable[[Callable[P, Any]], ExprFactory[P]]:
    first_param = next(iter(inspect.signature(calc_func).parameters))
    if first_param != "series":
        raise ValueError(f"Expected a series kernel, got {calc_func.__name__!r}")

    output_type = _get_output_type(calc_func)

    def decorator(func):
        name = func.__name__.lower()
        signature = inspect.signature(func)

        def wrapper(*args, **kwargs):
            if args and isinstance(args[0], pl.Expr):
                if "src" in kwargs:
                    raise ValueError("Cannot specify 'src' as a keyword argument when using a positional Polars expression.")
                kwargs["src"] = args[0]
                args = args[1:]

            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments = dict(bound_args.arguments)
            source = get_series_expr(arguments.pop("src"))

            def batch_func(data):
                return _wrap_batch_output(calc_func(data, **arguments))

            return source.map_batches(batch_func, return_dtype=output_type).alias(name)

        return _update_wrapper(wrapper, func, calc_func, signature)

    return decorator


def wrap_columns_expression(calc_func) -> Callable[[Callable[P, Any]], Callable[P, pl.Expr]]:
    inputs = _get_inputs(calc_func)
    params = tuple(inspect.signature(calc_func).parameters)
    if params[: len(inputs)] != inputs:
        raise ValueError(f"Column inputs do not match parameters for {calc_func.__name__!r}")

    output_type = _get_output_type(calc_func)

    def decorator(func):
        name = func.__name__.lower()
        signature = inspect.signature(func)

        def wrapper(*args, **kwargs):
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments = dict(bound_args.arguments)
            sources = [
                get_input_expr(arguments.pop(input_name), input_name)
                for input_name in inputs
            ]

            def batch_func(columns):
                return _wrap_batch_output(calc_func(*columns, **arguments))

            return pl.map_batches(
                sources,
                batch_func,
                return_dtype=output_type,
            ).alias(name)

        return _update_wrapper(wrapper, func, calc_func, signature)

    return decorator
