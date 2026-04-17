# mplchart indicator gap

Indicators present in mplchart but missing from mintalib (as of 2026-04-17).

All gaps have been resolved — no indicators are missing.

## Resolved

| Indicator | Notes |
|-----------|-------|
| **DONCHIAN** | Implemented in `src/mintalib/cython/donchian.pxi` |
| **ATRP** | Covered by `NATR` (normalized ATR = `atr / close * 100`) |

## Already covered (initial analysis was wrong)

`ADX`, `BBP`, `BBW`, `TSF`, `QSF`, `RVALUE` were already present in mintalib.
