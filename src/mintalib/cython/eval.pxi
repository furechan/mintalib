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
    elif hasattr(prices, 'sql'):
        query = f"SELECT ({expr}) FROM self"
        result = prices.sql(query)
    else:
        raise ValueError(f"Prices type {prices.__class__.__name__} not supported!")

    result = np.asarray(result, float)

    if as_flag:
        result = calc_flag(result)

    if wrap:
        result = wrap_result(result, prices)

    return result



