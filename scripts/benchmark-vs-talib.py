"""Speed benchmarks comparing mintalib vs TA-Lib.

Uses bundled daily OHLCV prices for direct-array calls and a synthetic
500-ticker Polars .over("ticker") workload. Both grouped backends use the
same map_batches adapter, including input conversion and NaN-to-null output
construction. Data construction and warmup are excluded from timings.
Some indicators differ in initialization/warmup; this is a speed comparison,
not a claim of exact numerical parity.

Usage:
    uv run python scripts/benchmark-vs-talib.py
    uv run python scripts/benchmark-vs-talib.py SMA
"""

import argparse
import timeit

import numpy as np
import polars as pl

try:
    import talib
except ImportError:
    raise SystemExit("ta-lib is not installed. Run: uv add --dev ta-lib")

from mintalib import core
from mintalib.samples import sample_prices


class Prices(dict):
    """Minimal prices object accepted by mintalib core functions (dict with array values)."""
    def __init__(self, open_, high, low, close, volume):
        super().__init__(open=open_, high=high, low=low, close=close, volume=volume)


def talib_zlema(ta, series, period):
    """Compose ZLEMA from TA-Lib EMA and the standard de-lagged input."""

    lag = (period - 1) // 2
    data = np.empty_like(series)
    data[:lag] = np.nan
    data[lag:] = 2 * series[lag:] - series[:-lag]
    return ta.EMA(data, period)


BENCHMARKS = [
    ("ADX(14)",   lambda ta, _, p: ta.ADX(p['high'], p['low'], p['close'], 14),
                                                                lambda _, p: core.calc_adx(p['high'], p['low'], p['close'], 14)),
    ("ATR(14)",   lambda ta, _, p: ta.ATR(p['high'], p['low'], p['close'], 14),
                                                                lambda _, p: core.calc_atr(p['high'], p['low'], p['close'], 14)),
    ("BOP()",     lambda ta, _, p: ta.BOP(p['open'], p['high'], p['low'], p['close']),
                                                                lambda _, p: core.calc_bop(p['open'], p['high'], p['low'], p['close'])),
    ("CCI(20)",   lambda ta, _, p: ta.CCI(p['high'], p['low'], p['close'], 20),
                                                                lambda _, p: core.calc_cci(p['high'], p['low'], p['close'], 20)),
    ("DEMA(20)",  lambda ta, c, _: ta.DEMA(c, 20),             lambda c, _: core.calc_dema(c, 20)),
    ("EMA(20)",   lambda ta, c, _: ta.EMA(c, 20),              lambda c, _: core.calc_ema(c, 20)),
    ("LINREG(20)", lambda ta, c, _: ta.LINEARREG(c, 20),       lambda c, _: core.calc_linreg(c, 20)),
    ("MACD(12,26,9)", lambda ta, c, _: ta.MACD(c, 12, 26, 9), lambda c, _: core.calc_macd(c, 12, 26, 9)),
    ("MAD(14)",   lambda ta, c, _: ta.AVGDEV(c, 14),           lambda c, _: core.calc_mad(c, 14)),
    ("MAX(20)",   lambda ta, c, _: ta.MAX(c, 20),              lambda c, _: core.calc_max(c, 20)),
    ("MDI(14)",   lambda ta, _, p: ta.MINUS_DI(p['high'], p['low'], p['close'], 14),
                                                                lambda _, p: core.calc_mdi(p['high'], p['low'], p['close'], 14)),
    ("MFI(14)",   lambda ta, _, p: ta.MFI(p['high'], p['low'], p['close'], p['volume'], 14),
                                                                lambda _, p: core.calc_mfi(p['high'], p['low'], p['close'], p['volume'], 14)),
    ("MIN(20)",   lambda ta, c, _: ta.MIN(c, 20),              lambda c, _: core.calc_min(c, 20)),
    ("PDI(14)",   lambda ta, _, p: ta.PLUS_DI(p['high'], p['low'], p['close'], 14),
                                                                lambda _, p: core.calc_pdi(p['high'], p['low'], p['close'], 14)),
    ("ROC(10)",   lambda ta, c, _: ta.ROC(c, 10),              lambda c, _: core.calc_roc(c, 10)),
    ("RSI(14)",   lambda ta, c, _: ta.RSI(c, 14),              lambda c, _: core.calc_rsi(c, 14)),
    ("SMA(20)",   lambda ta, c, _: ta.SMA(c, 20),              lambda c, _: core.calc_sma(c, 20)),
    ("STDEV(20)", lambda ta, c, _: ta.STDDEV(c, 20),           lambda c, _: core.calc_stdev(c, 20)),
    ("STOCH(14,3,3)", lambda ta, _, p: ta.STOCH(p['high'], p['low'], p['close'], 14, 3, 0, 3, 0),
                                                                lambda _, p: core.calc_stoch(p['high'], p['low'], p['close'], 14, 3, 3)),
    ("SUM(20)",   lambda ta, c, _: ta.SUM(c, 20),              lambda c, _: core.calc_sum(c, 20)),
    ("TEMA(20)",  lambda ta, c, _: ta.TEMA(c, 20),             lambda c, _: core.calc_tema(c, 20)),
    ("WMA(20)",   lambda ta, c, _: ta.WMA(c, 20),              lambda c, _: core.calc_wma(c, 20)),
    ("ZLEMA(20)", lambda ta, c, _: talib_zlema(ta, c, 20),    lambda c, _: core.calc_zlema(c, 20)),
]


def bench(fn, *args, repeat=5, number=10):
    times = timeit.repeat(lambda: fn(*args), repeat=repeat, number=number)
    return min(times) / number


def fmt_ms(seconds):
    return f"{seconds * 1000:.2f} ms"


# Pass only the arrays each indicator uses, identically for both backends.
PRICE_INPUTS = {
    "ADX": ("high", "low", "close"),
    "ATR": ("high", "low", "close"),
    "BOP": ("open", "high", "low", "close"),
    "CCI": ("high", "low", "close"),
    "MDI": ("high", "low", "close"),
    "MFI": ("high", "low", "close", "volume"),
    "PDI": ("high", "low", "close"),
    "STOCH": ("high", "low", "close"),
}


def grouped_expr(fn, inputs, fields):
    """Identical Polars bridge for either library's benchmark callback."""
    dtype = pl.Struct({field: pl.Float64 for field in fields}) if fields else pl.Float64

    def batch(columns):
        arrays = {name: np.asarray(column, dtype=np.float64) for name, column in zip(inputs, columns)}
        result = fn(arrays["close"], arrays)
        if fields:
            return pl.DataFrame(result, schema=fields, orient="col", nan_to_null=True).to_struct()
        return pl.Series(result, nan_to_null=True)

    return pl.map_batches([pl.col(name) for name in inputs], batch, return_dtype=dtype).over("ticker").alias("result")


def print_table(cases, *, repeat, number):
    print(f"{'Indicator':<15}  {'mintalib':>10}  {'ta-lib':>10}  {'ratio':>7}")
    print("-" * 49)
    ratios = []
    for name, mt_call, ta_call in cases:
        mt_call()
        ta_call()
        timings = [[], []]
        calls = (mt_call, ta_call)
        for iteration in range(repeat):
            for index in ((0, 1) if iteration % 2 == 0 else (1, 0)):
                timings[index].append(bench(calls[index], repeat=1, number=number))
        t_mt, t_ta = (min(values) for values in timings)
        ratio = t_mt / t_ta
        ratios.append(ratio)
        print(f"{name:<15}  {fmt_ms(t_mt):>10}  {fmt_ms(t_ta):>10}  {ratio:>7.2f}")
    if len(ratios) > 1:
        print(f"\nAverage ratio (mintalib/talib): {sum(ratios) / len(ratios):.2f}")
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("indicator", nargs="?", help="filter by indicator name (exact, case-insensitive)")
    parser.add_argument("--repeat", type=int, default=5, help="timeit repeat (default: 5)")
    parser.add_argument("--number", type=int, default=10, help="timeit number (default: 10)")
    parser.add_argument("--no-over", action="store_true", help="skip the 500-ticker Polars table")
    parser.add_argument("--over-number", type=int, default=1, help="grouped calls per repeat (default: 1)")
    args = parser.parse_args()
    if min(args.repeat, args.number, args.over_number) < 1:
        parser.error("repeat and number values must be positive")

    benchmarks = BENCHMARKS
    if args.indicator:
        key = args.indicator.upper()
        benchmarks = [(n, tf, mf) for n, tf, mf in BENCHMARKS if n.upper().split("(")[0] == key]
        if not benchmarks:
            raise SystemExit(f"No benchmark found for {args.indicator!r}")

    df = sample_prices()
    close = df.close.values.astype(float)
    prices = Prices(df.open.values.astype(float), df.high.values.astype(float),
                    df.low.values.astype(float), close, df.volume.values.astype(float))

    print(f"\nSingle ticker — direct arrays: {len(df):,} rows | repeat={args.repeat} number={args.number}\n")
    cases = [
        (name, lambda fn=mt_fn: fn(close, prices), lambda fn=ta_fn: fn(talib, close, prices))
        for name, ta_fn, mt_fn in benchmarks
    ]
    print_table(cases, repeat=args.repeat, number=args.number)

    if args.no_over:
        return

    frame = pl.DataFrame(prices)
    dataset = pl.concat([
        frame.select(pl.lit(f"T{i:03d}").alias("ticker"), pl.all())
        for i in range(1, 501)
    ]).rechunk()
    print(f"500 tickers — Polars .over('ticker'): {dataset.height:,} rows | workers={pl.thread_pool_size()} | repeat={args.repeat} number={args.over_number}\n")
    cases = []
    for name, ta_fn, mt_fn in benchmarks:
        inputs = PRICE_INPUTS.get(name.split("(")[0], ("close",))
        fields = getattr(mt_fn(close, prices), "_fields", ())
        mt_expr = grouped_expr(mt_fn, inputs, fields)
        ta_expr = grouped_expr(lambda c, p, fn=ta_fn: fn(talib, c, p), inputs, fields)
        cases.append((name, lambda expr=mt_expr: dataset.select(expr), lambda expr=ta_expr: dataset.select(expr)))
    print_table(cases, repeat=args.repeat, number=args.over_number)


if __name__ == "__main__":
    main()
