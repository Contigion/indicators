import pytest  # pylint: disable=unused-import
from contigion_indicators.sma import sma_crossover, sma_trend
from contigion_indicators.util.functions import get_dataframe_size
from .setup import data, n_candles

fast = 5
slow = 13
period = 200


def test_sma_crossover():
    sma_data = sma_crossover(data, fast, slow).drop(columns=['signal']).dropna(inplace=False)
    assert (get_dataframe_size(sma_data) == (n_candles - slow + 1))


def test_sma_trend():
    sma_data = sma_trend(data, period).drop(columns=['signal']).dropna(inplace=False)
    assert (get_dataframe_size(sma_data) == (n_candles - period + 1))
