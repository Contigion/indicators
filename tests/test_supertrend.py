import pytest  # pylint: disable=unused-import
from contigion_indicators.supertrend import supertrend, supertrend_direction
from contigion_indicators.util.functions import get_dataframe_size
from contigion_indicators.util.metatrader import get_market_data, connect


def test_supertrend():
    n_candles = 500
    atr_length = 7
    multiplier = 3
    offset = 0

    connect()
    data = get_market_data(number_of_candles=n_candles)
    supertrend_data = supertrend(data, atr_length, multiplier, offset).dropna(inplace=False)

    assert (get_dataframe_size(supertrend_data) == (n_candles - atr_length - 1))


def test_supertrend_direction():
    n_candles = 500
    atr_length = 7
    multiplier = 3
    offset = 0

    connect()
    data = get_market_data(number_of_candles=n_candles)
    supertrend_data = supertrend_direction(data, atr_length, multiplier, offset).drop(columns=['signal']).dropna(
        inplace=False)

    assert (get_dataframe_size(supertrend_data) == (n_candles - atr_length - 1))
