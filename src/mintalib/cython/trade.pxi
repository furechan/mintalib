""" Trade Indicator """


@export
class TRADE(Indicator):
    """
    Trade Indicator

    It adds/joins a pos column to an indicator together with the original price data,
    making the indicator act as a strategy.
    """

    def __init__(self, item=None, *, parent=None):
        self.parent = parent
        self.item = item

    def __ror__(self, parent):
        if self.parent is not None:
            return NotImplemented

        return self.__class__(item=self.item, parent=parent)

    def calc(self, prices):
        if self.parent:
            data = self.parent(prices)
        else:
            data = prices

        data = self.get_series(data)

        pos = np.where(data > 0.0, 1.0, 0.0)
        prices = prices.assign(pos=pos)

        return prices
