""" Money Flow Index """



@export
def calc_mfi(prices, long period = 14):
    """ Money Flow Index """

    prc = calc_typprice(prices)
    volume = asarray(prices['volume'], float)

    flow = prc * volume
    pflow = np.clip(flow, 0.0, None)
    nflow = -np.clip(flow, None, 0.0)

    with np.errstate(divide='ignore'):
        ratio = calc_sum(pflow, period) / calc_sum(nflow, period)
        result = 100 - 100 / (1 + ratio)

    result = wrap_result(result, prices)

    return result


class MFI(Indicator):
    """ Money Flow Index """

    def __init__(self, period: int = 14):
        self.period = period

    def calc(self, prices):
        result = calc_mfi(prices, period = self.period)
        return result


