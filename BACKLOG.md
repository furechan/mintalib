# Backlog

Items decided or considered but not scheduled. Add new items at the end.

## Indicators

- RSI null handling is inconsistent with EMA: EMA skips a null (carrying the average across the gap), but RSI re-seeds `prev` on a null, breaking the delta chain so the price move across the gap is not measured. Update RSI to keep `prev` across nulls (bridge) so it is consistent with the EMA/RMA skip behavior. Surfaced by bartons, which deliberately chose bridge for this reason (see bartons CHANGELOG 0.1.0).

