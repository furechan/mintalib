""" Expression eval """

def calc_eval(prices, expr: str):
    """
    Expression Eval (pandas only)

    Args:
        expr (str) : expression to eval
    """

    return prices.eval(expr)

