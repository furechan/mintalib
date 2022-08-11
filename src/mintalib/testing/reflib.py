""" reference implementation of technical analysis indicators based on talib/pandas/etc ... """

import pandas as pd

import talib

from talib import abstract

map_names = {
    'roc': 'ROCP',
    'psar': 'SAR'
}


class AbstractWrapper:
    def __init__(self, name):
        self.name = name
        self.function = getattr(abstract, name)

    def __call__(self, data, *args, **kwargs):
        if isinstance(data, pd.Series):
            data = data.rename('close').to_frame()

        return self.function(data, *args, **kwargs)


def get_ref(name):
    ref = globals().get(f"calc_{name}")
    if ref is not None:
        return ref

    name = map_names.get(name, name.upper())

    if hasattr(abstract, name):
        return AbstractWrapper(name)

    return None


def calc_macd(series, n1=12, n2=26, n3=9):
    ema1 = talib.EMA(series, n1)
    ema2 = talib.EMA(series, n2)

    macd = ema1 - ema2
    signal = talib.EMA(macd, n3)
    hist = macd - signal

    result = dict(macd=macd, macdsignal=signal, macdhist=hist)

    return pd.DataFrame(result)


def calc_ppo(series, n1=12, n2=26, n3=9):
    ema1 = talib.EMA(series, n1)
    ema2 = talib.EMA(series, n2)

    ppo = (ema1 / ema2 - 1.0) * 100
    signal = talib.EMA(ppo, n3)
    hist = ppo - signal

    result = dict(ppo=ppo, pposignal=signal, ppohist=hist)

    return pd.DataFrame(result)
