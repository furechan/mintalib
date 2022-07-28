""" Rate of Change """


def calc_roc(series, int period=1):
    result = series.pct_change(period)
    return result


class ROC(Indicator):
    """ Rate of Change """

    def __init__(self, period=12, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_roc(series, self.period)
        return result
