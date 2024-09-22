""" Expression eval """

def calc_eval(prices, expr: str):
    """Expression Eval (pandas only)"""

    return prices.eval(expr).astype(float)


@wrap_function(calc_eval)
def EVAL(prices, expr: str):
    result = calc_eval(prices, expr=expr)
    return wrap_result(result, prices)

