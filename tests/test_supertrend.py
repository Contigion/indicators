import pytest  # pylint: disable=unused-import
from contigion_indicators.supertrend import supertrend, supertrend_trend
from contigion_indicators.util.functions import get_dataframe_size
from .setup import data, n_candles

atr_length = 7
multiplier = 3
offset = 0


def test_supertrend():
    supertrend_data = supertrend(data, atr_length, multiplier, offset).dropna(inplace=False)
    assert (get_dataframe_size(supertrend_data) == (n_candles - atr_length))


def test_supertrend_direction():
    supertrend_data = supertrend_trend(data, atr_length, multiplier, offset).drop(columns=['signal']).dropna(
        inplace=False)
    assert (get_dataframe_size(supertrend_data) == (n_candles - atr_length))
