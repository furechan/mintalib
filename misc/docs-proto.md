# `mintalib.functions` module

Mitalib functions

## `to_md_file` function

```python
to_md_file(
    markdown_str: str,
    filename: str,
    out_path: str = '.',
    watermark: bool = True,
    disable_markdownlint: bool = True
) → None
```

Exponential Moving Average

Args
- period : time period, required
- adjust : whether to adjust weights, default False
    when true update ratio increases gradually (see formula)
    
Formula
- EMA is calculated as a recursive formula
- The standard formula is ema += alpha * (value - ema)
    with alpha = 2.0 / (period + 1.0)
- The adjusted formula is ema = num/div
    where num = value + rho * num, div = 1.0 + rho * div
    with rho = 1.0 - alpha

Attributes
- same_scale = True


