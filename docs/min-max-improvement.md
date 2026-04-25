# Rolling Min/Max Improvement

## Problem

The original `calc_min` and `calc_max` used a naive nested loop — rescanning the
full window from scratch for every output bar:

```cython
for i in range(maxlen):       # O(n)
    for j in range(period):   # O(period) every bar
        ...
```

O(n × period) total. TA-Lib uses a monotonic deque (O(n)), giving it a ~4x
advantage at period=20.

## Fix: compare to prior extremum, rescan only on expiry

Track the current extremum and its index. On each new bar:

- If the prior extremum index is still inside the window, just compare the new
  value against it — O(1) per bar in the common case.
- If the prior extremum fell out of the window, rescan — O(period) but rare on
  real price data where extremes are stable.

```cython
if max_idx >= i - period + 1:
    if not v <= cur_max:
        cur_max = v
        max_idx = i
else:
    # rescan
    cur_max = NAN
    max_idx = -1
    for j in range(i - period + 1, i + 1):
        v = xs[j]
        if not isnan(v) and not v <= cur_max:
            cur_max = v
            max_idx = j

output[i] = cur_max
```

## Why not the monotonic deque?

The full O(n) monotonic deque was implemented and tested but was slower on real
price data (ratio 3.26 vs 2.09 for MAX). The `% period` modulo on every push/pop
costs more than it saves, because on real OHLCV data the extremum rarely falls out
of the window. The simpler approach wins in practice.

The deque would be preferable on adversarial/random data where the extremum
changes every bar.

## Results

| Indicator | Before | After |
|-----------|--------|-------|
| MAX(20)   | 4.35   | 2.09  |
| MIN(20)   | 3.39   | 2.29  |

Ratios are mintalib/talib — lower is better. Still behind TA-Lib's deque but
roughly halved from the original.

## Applicability

Same pattern applies to any rolling extremum kernel in barcalc or similar.
The key variables to track: `cur_max` / `cur_min` and `max_idx` / `min_idx`.
