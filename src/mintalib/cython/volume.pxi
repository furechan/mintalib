""" Exponential Moving Average """


@export
class VOLUME(Indicator):
    """ Volume """

    item = 'volume'

    def __init__(self, sma=0):
        self.sma = sma

    def calc(self, data):
        volume = self.get_series(data)
        result = volume.to_frame()

        if 'close' in data:
            if 'open' in data:
                change = data.close/data.open - 1.0
            else:
                change = data.close.pct_change()
            result = result.assign(change=change)

        if self.sma:
            average = calc_sma(volume, self.sma)
            result = result.assign(average=average)

        return result

