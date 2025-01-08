import pytest  # pylint: disable=unused-import
from contigion_indicators.bollinger_bands import bollinger_bands_cross
from contigion_indicators.util.functions import get_dataframe_size
from .setup import data, n_candles

period = 7


def test_bollinger_bands():
    bb_data = bollinger_bands_cross(data, period).drop(columns=['signal']).dropna(inplace=False)
    assert (get_dataframe_size(bb_data) == (n_candles - period + 1))
