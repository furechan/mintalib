""" Ganeric Moving Average """

cdef enum:
    MA_TYPE_SMA = 0
    MA_TYPE_EMA = 1
    MA_TYPE_WMA = 2
    MA_TYPE_RMA = 3
    MA_TYPE_DEMA = 4
    MA_TYPE_TEMA = 5

@export
class MA_Type(IntEnum):
    """ Moving Average Type Enumeration """

    def __repr__(self):
        return self.name
    SMA = 0
    EMA = 1
    WMA = 2
    RMA = 3
    DEMA = 4
    TEMA = 5


@export
def calc_ma(series, long period=20, int ma_type=0):
    """
    Generic Moving Average

    Args:
        period (int) : time period. default 20
        ma_type (int) : type of moving average. default 0 (SMA)
    """

    if ma_type == MA_TYPE_SMA:
        return calc_sma(series, period)

    if ma_type == MA_TYPE_EMA:
        return calc_ema(series, period)

    if ma_type == MA_TYPE_WMA:
        return calc_wma(series, period)

    if ma_type == MA_TYPE_RMA:
        return calc_rma(series, period)

    if ma_type == MA_TYPE_DEMA:
        return calc_dema(series, period)

    if ma_type == MA_TYPE_TEMA:
        return calc_tema(series, period)

    raise ValueError(f"Invalid ma_type {ma_type}")
