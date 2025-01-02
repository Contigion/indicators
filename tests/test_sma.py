import pytest  # pylint: disable=unused-import
import pandas as pd
from contigion_indicators.sma import sma_crossover, sma_trend_direction
from contigion_indicators.util.functions import get_dataframe_size


def test_sma_crossover():
    n_candles = 500
    fast = 5
    slow = 13

    data = pd.read_csv('resources/data.csv')
    sma_data = sma_crossover(data, fast, slow).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(sma_data) == (n_candles - slow))


def test_sma_trend():
    n_candles = 500
    period = 200

    data = pd.read_csv('resources/data.csv')
    sma_data = sma_trend_direction(data, period).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(sma_data) == (n_candles - period))
