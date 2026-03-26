""" Expression eval """

def calc_eval(prices, unicode expr, *, bint as_flag=False):
    """
    Expression Eval

    Evaluates an expression against the prices dataframe.
    Uses `DataFrame.eval` for pandas and `DataFrame.sql` for polars.

    Args:
        expr (str) : expression to eval
        as_flag (bool) : whether to return result as a flag value
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

    return result



