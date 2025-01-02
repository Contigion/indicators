import pytest  # pylint: disable=unused-import
import pandas as pd
from contigion_indicators.macd import macd_crossover
from contigion_indicators.util.functions import get_dataframe_size


def test_maccd_crossover():
    n_candles = 500
    fast = 12
    slow = 26
    signal = 9

    data = pd.read_csv('data.csv')
    macd_data = macd_crossover(data, fast, slow, signal).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(macd_data) == (n_candles - slow - signal + 1))
