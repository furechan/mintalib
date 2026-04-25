"""Speed benchmarks comparing mintalib vs TA-Lib.

Uses bundled sample prices (daily OHLCV, ~11k rows).
Only covers indicators where both libraries produce equivalent results.

Usage:
    uv run python scripts/benchmark-vs-talib.py
    uv run python scripts/benchmark-vs-talib.py SMA
"""

import argparse
import timeit

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


BENCHMARKS = [
    ("SMA(20)",   lambda ta, c, _: ta.SMA(c, 20),              lambda c, _: core.calc_sma(c, 20)),
    ("EMA(20)",   lambda ta, c, _: ta.EMA(c, 20),              lambda c, _: core.calc_ema(c, 20)),
    ("WMA(20)",   lambda ta, c, _: ta.WMA(c, 20),              lambda c, _: core.calc_wma(c, 20)),
    ("DEMA(20)",  lambda ta, c, _: ta.DEMA(c, 20),             lambda c, _: core.calc_dema(c, 20)),
    ("TEMA(20)",  lambda ta, c, _: ta.TEMA(c, 20),             lambda c, _: core.calc_tema(c, 20)),
    ("RSI(14)",   lambda ta, c, _: ta.RSI(c, 14),              lambda c, _: core.calc_rsi(c, 14)),
    ("STDEV(20)", lambda ta, c, _: ta.STDDEV(c, 20),           lambda c, _: core.calc_stdev(c, 20)),
    ("MAD(14)",   lambda ta, c, _: ta.AVGDEV(c, 14),           lambda c, _: core.calc_mad(c, 14)),
    ("MAX(20)",   lambda ta, c, _: ta.MAX(c, 20),              lambda c, _: core.calc_max(c, 20)),
    ("MIN(20)",   lambda ta, c, _: ta.MIN(c, 20),              lambda c, _: core.calc_min(c, 20)),
    ("SUM(20)",   lambda ta, c, _: ta.SUM(c, 20),              lambda c, _: core.calc_sum(c, 20)),
    ("ATR(14)",   lambda ta, _, p: ta.ATR(p['high'], p['low'], p['close'], 14),
                                                                lambda _, p: core.calc_atr(p, 14)),
    ("CCI(20)",   lambda ta, _, p: ta.CCI(p['high'], p['low'], p['close'], 20),
                                                                lambda _, p: core.calc_cci(p, 20)),
    ("MFI(14)",   lambda ta, _, p: ta.MFI(p['high'], p['low'], p['close'], p['volume'], 14),
                                                                lambda _, p: core.calc_mfi(p, 14)),
    ("TRANGE",    lambda ta, _, p: ta.TRANGE(p['high'], p['low'], p['close']),
                                                                lambda _, p: core.calc_trange(p)),
]


def bench(fn, *args, repeat=5, number=10):
    times = timeit.repeat(lambda: fn(*args), repeat=repeat, number=number)
    return min(times) / number


def fmt_ms(seconds):
    return f"{seconds * 1000:.2f} ms"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("indicator", nargs="?", help="filter by indicator name (exact, case-insensitive)")
    parser.add_argument("--repeat", type=int, default=5, help="timeit repeat (default: 5)")
    parser.add_argument("--number", type=int, default=10, help="timeit number (default: 10)")
    args = parser.parse_args()

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

    print(f"\nRows: {len(df):,}  |  repeat={args.repeat}  number={args.number}\n")
    print(f"{'Indicator':<12}  {'mintalib':>10}  {'ta-lib':>10}  {'ratio':>7}")
    print("-" * 46)

    ratios = []
    for name, ta_fn, mt_fn in benchmarks:
        t_mt = bench(mt_fn, close, prices, repeat=args.repeat, number=args.number)
        t_ta = bench(ta_fn, talib, close, prices, repeat=args.repeat, number=args.number)
        ratio = t_mt / t_ta
        ratios.append(ratio)
        print(f"{name:<12}  {fmt_ms(t_mt):>10}  {fmt_ms(t_ta):>10}  {ratio:>7.2f}")

    if len(ratios) > 1:
        avg = sum(ratios) / len(ratios)
        print(f"\nAverage ratio (mintalib/talib): {avg:.2f}")
    print()


if __name__ == "__main__":
    main()
