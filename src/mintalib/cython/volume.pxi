""" Exponential Moving Average """


@export
class VOLUME(Indicator):
    """ Volume """

    item = 'volume'

    def __init__(self):
        pass

    def calc(self, data):
        result = self.get_series(data)
        return result

