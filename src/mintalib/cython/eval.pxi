""" Expression eval """

def calc_eval(prices, expr: str):
    """
    Expression Eval (pandas only)

    Args:
        expr (str) : expression to eval
    """

    # Coerce to float to avoid boolean series
    return prices.eval(expr).astype(float)

