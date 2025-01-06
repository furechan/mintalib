""" Expression eval """

def calc_eval(prices, expr: str):
    """
    Expression Eval (pandas only)

    Args:
        expr (str) : expression to eval
    """

    return prices.eval(expr)


@wrap_function(calc_eval)
def EVAL(prices, expr: str):
    return calc_eval(prices, expr=expr)

