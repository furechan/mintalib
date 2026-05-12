# Cython Compiler Directives — Impact on Performance

## Directives added

Added to the top of `src/mintalib/core.pyx` (applies to all included `.pxi` files):

```python
# cython: boundscheck=False, wraparound=False, cdivision=True, nonecheck=False
```

## What each does

- **`boundscheck=False`** — skips array index range checks on every memoryview access
- **`wraparound=False`** — disables negative-index support
- **`cdivision=True`** — uses C division semantics (no Python `ZeroDivisionError` guard)
- **`nonecheck=False`** — skips None checks on typed variables

## Measured impact (daily sample prices, ~11k rows)

| Indicator | Without | With | Change |
|-----------|---------|------|--------|
| SMA(20)   | 0.93    | 0.75 | -19%   |
| EMA(20)   | 1.03    | 1.04 | —      |
| WMA(20)   | 1.49    | 1.32 | -11%   |
| DEMA(20)  | 1.22    | 1.19 | —      |
| TEMA(20)  | 1.26    | 1.21 | —      |
| RSI(14)   | 1.51    | 1.51 | —      |
| STDEV(20) | 1.42    | 1.42 | —      |
| MAD(14)   | 0.92    | 0.76 | -17%   |
| MAX(20)   | 4.47    | 4.35 | —      |
| MIN(20)   | 3.58    | 3.39 | —      |
| SUM(20)   | 1.36    | 1.35 | —      |
| ATR(14)   | 0.70    | 0.70 | —      |
| CCI(20)   | 1.00    | 0.85 | -15%   |
| MFI(14)   | 2.33    | 2.19 | —      |
| TRANGE    | 3.11    | 3.02 | —      |
| **Average** | **1.76** | **1.67** | **-5%** |

Ratios are mintalib/talib — lower is better.

## Conclusion

Overall ~5% improvement in average ratio. Indicators with dense inner loops and
frequent memoryview access (SMA, MAD, CCI) benefit most. Indicators bottlenecked
elsewhere (MAX, MIN, TRANGE, RSI) see little change.
