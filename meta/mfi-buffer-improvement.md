# MFI Circular Buffer Improvement

## Problem

The original `calc_mfi` was composed from multiple numpy operations:

```python
prc = calc_typprice(prices)
roc = calc_roc(prc, 1)
flow = prc * volume * np.sign(roc)
pflow = np.clip(flow, 0.0, None)
nflow = -np.clip(flow, None, 0.0)
ratio = calc_sum(pflow, period) / calc_sum(nflow, period)
result = 100 - 100 / (1 + ratio)
```

Six separate passes over the data, each allocating a temporary array.
TA-Lib uses a single C loop with a circular buffer of `MoneyFlow` structs —
confirmed by reading `ta_MFI.c`.

## Fix: single Cython loop with circular buffer

Track `psum` and `nsum` as running totals. Store each bar's signed flow in a
circular buffer so the oldest bar can be subtracted when it falls out of the
window:

```cython
drop = buf[buf_idx]
if drop > 0.0:
    psum -= drop
elif drop < 0.0:
    nsum += drop        # drop is negative → subtracts from nsum

buf[buf_idx] = flow
if flow > 0.0:
    psum += flow
elif flow < 0.0:
    nsum -= flow        # flow is negative → adds abs(flow) to nsum

buf_idx += 1
if buf_idx >= period:
    buf_idx = 0
```

Positive flow (typ > prev_typ) stored as `+mf`, negative flow as `-mf`, flat as `0`.
One pass, no temporaries.

## Results

| Indicator | Before | After |
|-----------|--------|-------|
| MFI(14)   | 2.07   | 1.01  |

Ratios are mintalib/talib — lower is better.
