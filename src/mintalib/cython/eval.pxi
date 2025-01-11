""" Expression eval """

def calc_eval(prices, expr: str, *, as_flag: bool = False):
    """
    Expression Eval (pandas only)

    Args:
        expr (str) : expression to eval
    """

    # Coerce to float to avoid boolean series

    if hasattr(prices, 'eval'):
        result = prices.eval(expr).astype(float)
    elif expr in prices:
        result = prices[expr]
    else:
        raise ValueError(f"Expression {expr!r} not supported!")

    if as_flag:
        result = calc_flag(result, wrap=True)

    return result



