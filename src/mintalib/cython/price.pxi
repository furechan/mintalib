""" Exponential Moving Average """


# TODO re-implement without pandas logic ?

@export
def calc_mid(prices):
    """ Calculates mid prices (used in calc_price) """

    result = prices.filter(['high', 'low', 'close']).mean(axis=1).rename('mid')
    return result


@export
def calc_log(prices):
    """ Calculates log prices (used in calc_price) """

    return np.log(prices.close).rename('log')


@export
def calc_price(prices, item='close'):
    """ looks up or calculates standard item """

    if item in prices:
        return prices.get(item)

    if item == 'mid':
        return calc_mid(prices)

    if item == 'log':
        return calc_log(prices)

    raise ValueError(f"Invalid item {item}") from None


@export
class PRICE(Indicator):
    """ Price Indicator """

    def __init__(self, item='close'):
        self.item = item

    def calc(self, data):
        result = calc_price(data, item=self.item)
        return result

