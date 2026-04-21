"""Speed benchmarks comparing mintalib vs TA-Lib.

Runs on a large synthetic price array to amplify timing differences.
Only covers indicators where both libraries produce equivalent results.

Usage:
    uv run python scripts/benchmark-vs-talib.py
    uv run python scripts/benchmark-vs-talib.py --size 500000
"""

import argparse
import timeit
import numpy as np

try:
    import talib
except ImportError:
    raise SystemExit("ta-lib is not installed. Run: uv add --dev ta-lib")

from mintalib import core


def make_prices(n, seed=42):
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    high = close + rng.uniform(0, 2, n)
    low = close - rng.uniform(0, 2, n)
    open_ = close + rng.normal(0, 0.5, n)
    volume = rng.uniform(1e6, 1e7, n)
    return open_, high, low, close, volume


class Prices(dict):
    """Minimal prices object accepted by mintalib core functions (dict with array values)."""
    def __init__(self, open_, high, low, close, volume):
        super().__init__(open=open_, high=high, low=low, close=close, volume=volume)


BENCHMARKS = [
    ("SMA(20)",   lambda ta, c, _: ta.SMA(c, 20),              lambda c, _: core.calc_sma(c, 20)),
    ("WMA(20)",   lambda ta, c, _: ta.WMA(c, 20),              lambda c, _: core.calc_wma(c, 20)),
    ("RSI(14)",   lambda ta, c, _: ta.RSI(c, 14),              lambda c, _: core.calc_rsi(c, 14)),
    ("STDEV(20)", lambda ta, c, _: ta.STDDEV(c, 20),           lambda c, _: core.calc_stdev(c, 20)),
    ("MAD(14)",   lambda ta, c, _: ta.AVGDEV(c, 14),           lambda c, _: core.calc_mad(c, 14)),
    ("MAX(20)",   lambda ta, c, _: ta.MAX(c, 20),              lambda c, _: core.calc_max(c, 20)),
    ("MIN(20)",   lambda ta, c, _: ta.MIN(c, 20),              lambda c, _: core.calc_min(c, 20)),
    ("SUM(20)",   lambda ta, c, _: ta.SUM(c, 20),              lambda c, _: core.calc_sum(c, 20)),
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
    parser.add_argument("--size", type=int, default=100_000, help="array size (default: 100000)")
    parser.add_argument("--repeat", type=int, default=5, help="timeit repeat (default: 5)")
    parser.add_argument("--number", type=int, default=10, help="timeit number (default: 10)")
    args = parser.parse_args()

    open_, high, low, close, volume = make_prices(args.size)
    prices = Prices(open_, high, low, close, volume)

    print(f"\nArray size: {args.size:,}  |  repeat={args.repeat}  number={args.number}\n")
    print(f"{'Indicator':<12}  {'mintalib':>10}  {'ta-lib':>10}  {'speedup':>8}")
    print("-" * 46)

    for name, ta_fn, mt_fn in BENCHMARKS:
        t_mt = bench(mt_fn, close, prices, repeat=args.repeat, number=args.number)
        t_ta = bench(ta_fn, talib, close, prices, repeat=args.repeat, number=args.number)
        ratio = t_ta / t_mt
        marker = " <" if ratio < 1 else ""
        print(f"{name:<12}  {fmt_ms(t_mt):>10}  {fmt_ms(t_ta):>10}  {ratio:>7.1f}x{marker}")

    print()


if __name__ == "__main__":
    main()
