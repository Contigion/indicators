import pytest  # pylint: disable=unused-import
from contigion_indicators.macd import macd_crossover
from contigion_indicators.util.functions import get_dataframe_size
from .setup import data, n_candles

fast = 12
slow = 26
signal = 9


def test_maccd_crossover():
    macd_data = macd_crossover(data, fast, slow, signal).drop(columns=['signal']).dropna(inplace=False)
    assert (get_dataframe_size(macd_data) == (n_candles - slow - signal + 2))
