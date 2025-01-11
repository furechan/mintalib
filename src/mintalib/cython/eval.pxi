""" Expression eval """

def calc_eval(prices, expr: str):
    """
    Expression Eval (pandas only)

    Args:
        expr (str) : expression to eval
    """

    # Coerce to float to avoid boolean series

    if hasattr(prices, 'eval'):
        return prices.eval(expr).astype(float)

    if expr in prices:
        return prices[expr]

    raise ValueError(f"Expression {expr!r} not supported!")


