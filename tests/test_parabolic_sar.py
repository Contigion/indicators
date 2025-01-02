import pytest  # pylint: disable=unused-import
from contigion_indicators.parabolic_sar import psar_trend
from contigion_indicators.util.functions import get_dataframe_size
from .setup import data, n_candles


def test_psar_trend():
    sma_data = psar_trend(data)
    assert get_dataframe_size(sma_data) == n_candles
