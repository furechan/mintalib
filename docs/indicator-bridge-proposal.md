# Indicator Bridge Proposal: `as_expr()`

## Prerequisites

This proposal depends on [indicator-narrowing-proposal.md](indicator-narrowing-proposal.md).
Indicators must be narrowed to pandas-only before `as_expr()` is added.

The dependency is semantic, not technical: on a pandas/polars-agnostic indicator,
`as_expr()` would be ambiguous — it could mean a polars expression just as well as
a pandas one. The unqualified name `as_expr()` is only justified once the
indicator's identity is clearly pandas. Without the narrowing, the method would
need to be called `as_pandas_expr()` to be unambiguous.

## Background

mintalib has two parallel interfaces for computing indicators:

- `mintalib.indicators` — callable objects (`FuncIndicator`) that work with pandas DataFrames and Series. Used as `SMA(20)(df)` or `df | SMA(20)`.
- `mintalib.expressions` — polars expression factories that return `pl.Expr`. Used as `SMA(20)` in a polars `.select()` or `.with_columns()` context.

The proposal is to add an `as_expr()` method to the `Indicator` base class that bridges the indicators world to the pandas expression world introduced in pandas 3.0.

## Pandas Expressions (`pandas.api.typing.Expression`)

pandas 3.0 introduced `pd.col()` and the `Expression` class (`pandas.api.typing.Expression`). An `Expression` is a deferred computation: a callable `(DataFrame) -> Series` paired with a string label, with all Python operators overloaded to return new expressions.

```python
pd.col("close") < 30          # Expression: col('close') < 30
pd.col("close") * 2           # Expression: col('close') * 2
(pd.col("close") > 20) & (pd.col("close") < 50)  # compound
```

Expressions are consumed wherever pandas accepts a deferred column reference:

```python
df.assign(flag=pd.col("close") < 30)
df.loc[pd.col("close") > 25]
df[pd.col("close").between(20, 50)]  # via __getitem__
```

The `Expression` constructor is `Expression(func, repr_str)` where `func` is any `(DataFrame) -> Any` callable.

## `as_expr()` Method

Any `Indicator` already satisfies the `Expression` contract:
- It is callable: `indicator(df)` returns a pandas Series
- It has a repr: `repr(indicator)` returns e.g. `RSI(14)` or `EMA(20) | ROC(1)`

`as_expr()` is therefore a one-liner bridge on the base class:

```python
def as_expr(self):
    from pandas.api.typing import Expression
    return Expression(self, repr(self))
```

This makes the full `Expression` operator algebra available on any single-output indicator:

```python
RSI(14).as_expr() < 30                          # oversold
EMA(9).as_expr() > EMA(21).as_expr()            # bullish crossover condition
(RSI(14).as_expr() < 30) & (SMA(50).as_expr() > SMA(200).as_expr())

df.assign(oversold=RSI(14).as_expr() < 30)
df.loc[EMA(20).as_expr() > pd.col("close")]
```

## Rationale

The key insight is the semantic match: an `Expression` is a named callable `(DataFrame) -> Series`, and a `FuncIndicator` is exactly that. No wrapping, no reimplementation — the bridge is structural.

This also mirrors the polars side: in `mintalib.expressions`, `RSI(14)` already returns a `pl.Expr` directly. With `as_expr()`, the pandas side reaches the same expressiveness for signal composition.

## Limitations

**pandas version** — `pandas.api.typing.Expression` requires pandas 3.0+. On older versions `as_expr()` raises `NotImplementedError`.

**Multi-output indicators** — Indicators with multiple outputs (MACD, BBANDS, DONCHIAN, DMI, BBP/BBW pairs) return DataFrames rather than Series. pandas expressions have no public API to consume a multi-column result in `df.assign()` or `df.loc[]`. `as_expr()` raises `NotImplementedError` for these indicators. They remain usable as indicators; only `as_expr()` is blocked.

**`IndicatorChain`** — Chained indicators (`EMA(20) | ROC(1)`) support `as_expr()` for the same reason as `FuncIndicator`: the chain is callable and has a repr. If the chain's final indicator produces multiple outputs the expression will return a DataFrame at evaluation time, but that is a usage error rather than a structural limitation.
