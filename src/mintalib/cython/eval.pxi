""" Expression eval """

def calc_eval(prices, unicode expr, *, bint as_flag=False, bint wrap=False):
    """
    Expression Eval (pandas only)

    Args:
        expr (str) : expression to eval
    """

    # Coerce to float to avoid boolean series

    if hasattr(prices, 'eval'):
        result = prices.eval(expr)
        result = np.asarray(result, float)
    else:
        raise ValueError(f"Expression {expr!r} not supported!")

    if as_flag:
        result = calc_flag(result)

    if wrap:
        result = wrap_result(result, prices)

    return result



