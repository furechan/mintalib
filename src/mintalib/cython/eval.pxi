""" Expression Eval """


@export
class EVAL(Indicator):
    """ Expression Eval (pandas based) """

    def __init__(self, expr):
        self.expr = expr

    def calc(self, prices):
        return prices.eval(self.expr)

