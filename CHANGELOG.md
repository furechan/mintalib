# Change Log

## 0.0.26
- Added a `pandas` extension module `mintalib.pandas`
- Added a `polars` extension module `mintalib.polars`
- `functions` and `expressions` modules are legacy

## 0.0.25
- Added some expression tests
- Added `BBP` Indicator (Bolling Bands Percent)
- Added `BBW` Indicator (Bolling Bands Width)
- Added `MACDV` Indicator (MACD Volatility normalized)
- Modified `STREAK` Indicator. Counts values above zero
- Switched to `tox.toml`

## 0.0.24
- Added polars expressions (experimental)

## 0.0.23
- Refactored indicators as simple wrappers

## 0.0.22
- Added `QSF` Indicator (Quadratic Series Forecast)  

## 0.0.20
- Metadata is passing through to indicators via the `metadata` attribute
- Added `alias` method to FuncIndicator to set indicator output name

## 0.0.19
- Added `STEP` Indicator (Step Function)
- Added `CLAG` Indicator (Confirmation Lag)
- Added `LROC` Indicator (Logarithmic Rate of Change)
- Added `ALMA` Indicator (Arnaud Legoux Moving Average)
- Indicators `ROC` and `LROC` now accept a negative period

## 0.0.18
- Refactored `functions` module to move logic out of core. Function names are now small caps!
- Upper case functions names are legacy and will be removed in the future. Use small caps.

## 0.0.16
- Added `DMI` indicator with grouped calculation for `ADX`, `PDI` and `MDI`
- Renamed `PLUSDI`, `MINUSDI` to `PDI`, `MDI` 

## 0.0.15
- Fixed pypi-readme.md

## 0.0.13
- Added `CURVE` indicator

## 0.0.11
- Added docs

## 0.0.6
- Fixed `MANIFEST.ini`

## 0.0.4
- Indicators moved to `indicators` module
- Functions moved to `functions` module

## 0.0.3
- Functions implemented directly in core
- Setup with pyproject.toml
- Added tox.ini config

## 0.0.1
- Initial release
