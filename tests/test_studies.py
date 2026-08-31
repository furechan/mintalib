import pandas as pd

from mintalib.indicators import MACD, SMA
from mintalib.samples import sample_prices
from mintalib.studies import Study, Trail


def test_study_collects_named_and_multi_output_indicators():
    prices = sample_prices()
    study = Study(MACD(), sma20=SMA(20))

    result = prices.pipe(study)

    assert list(result.columns) == ["macd", "macdsignal", "macdhist", "sma20"]
    assert result.index.equals(prices.index)


def test_study_calc_returns_only_calculated_columns():
    prices = sample_prices()

    result = Study(sma20=SMA(20)).calc(prices)

    assert list(result.columns) == ["sma20"]


def test_study_can_merge_results_with_input():
    prices = sample_prices()
    study = Study(sma20=SMA(20))

    calculated = study.calc(prices, merge=True)
    piped = prices.pipe(study, merge=True)

    assert list(calculated.columns) == [*prices.columns, "sma20"]
    pd.testing.assert_frame_equal(calculated[prices.columns], prices)
    pd.testing.assert_frame_equal(piped, calculated)


def test_study_merge_overwrites_existing_columns():
    prices = sample_prices()

    result = prices.pipe(Study(close=SMA(20)), merge=True)

    assert list(result.columns) == list(prices.columns)
    pd.testing.assert_series_equal(result["close"], SMA(20)(prices), check_names=False)


def test_trail_uses_shared_merge_behavior():
    prices = sample_prices()

    result = prices.pipe(Trail("close", windows=2), merge=True)

    assert list(result.columns) == [*prices.columns, "close0", "close1"]
