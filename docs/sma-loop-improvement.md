# SMA Loop Improvement

## Problem

Several rolling-window Cython kernels tracked a `j` pointer and used a `while` loop
to remove the oldest element from the accumulator when the window was full:

```cython
while count > period and j < i:
    v, j = xs[j], j + 1
    if v == v:
        rsum -= v
        count -= 1
```

This pattern has two issues:

1. **Redundant loop structure.** `count` increases by at most 1 per outer iteration,
   so the `while` runs at most once — except when `j` lands on an old NaN position,
   in which case it needs to skip past it (no count decrement) and then subtract the
   next valid element (two steps). An `if` is not a safe replacement for this reason.

2. **Bug with mid-series NaN.** When a NaN resets `count = 0`, `j` is not reset.
   It stays pointing to old positions before the NaN gap. When count builds back up
   to `period + 1`, the `while` subtracts stale pre-NaN values instead of the correct
   oldest element in the new window.

## Fix

`count > period` with no NaN reset since the last drop guarantees that the last
`count` values (indices `i - count + 1` through `i`) are all non-NaN. Therefore
the element to drop is exactly `xs[i - period]` — known at compile time, no `j`
pointer needed, no NaN check needed on the dropped element.

Replace the `while` block with a single `if`:

```cython
if count > period:
    rsum -= xs[i - period]
    count -= 1
```

For kernels that track multiple accumulators (e.g. `stdev` tracks `sx` and `sxx`),
apply the same drop to each:

```cython
if count > period:
    x = xs[i - period]
    count -= 1
    sx -= x
    sxx -= x * x
```

For `wma`, the weight-shift step comes first, then drop the oldest value:

```cython
if count > period:
    wsum -= rsum
    rsum -= xs[i - period]
    count -= 1
```

## Kernels fixed in mintalib

| File | Accumulators dropped |
|------|----------------------|
| `sma.pxi` | `rsum` |
| `sum.pxi` | `rsum` |
| `stdev.pxi` | `sx`, `sxx` |
| `mad.pxi` | `sx` |
| `wma.pxi` | `wsum` (weight shift), `rsum` |

## Applicability

Any rolling-window kernel that:
- accumulates into one or more running sums
- resets all accumulators to 0 on NaN
- uses a `j` pointer + `while count > period` to drop the oldest element

can apply this fix. The `j` variable and its `cdef` declaration can be removed entirely.

Does **not** apply to kernels where the window drop requires accessing non-oldest
elements (e.g. min/max with a deque), or where the window is not NaN-reset-based.
