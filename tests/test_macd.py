import pytest  # pylint: disable=unused-import
from contigion_indicators.macd import *
from contigion_indicators.util.functions import get_dataframe_size
from contigion_indicators.util.metatrader import get_market_data, connect


def test_maccd_crossover():
    n_candles = 500
    fast = 12
    slow = 26
    signal = 9

    connect()
    data = get_market_data(number_of_candles=n_candles)
    macd_data = macd_crossover(data, fast, slow, signal).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(macd_data) == (n_candles - slow - signal + 1))
