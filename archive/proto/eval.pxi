""" Expression Eval """


class EVAL(Indicator):
    """
    Expression Eval (pandas only)

    Args:
        expr (str) : expression to evaluate on the dataframe, required
    """

    def __init__(self, expr):
        self.expr = expr

    def calc(self, prices):
        return prices.eval(self.expr).astype(float)

