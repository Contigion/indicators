import pytest  # pylint: disable=unused-import
from contigion_indicators.parabolic_sar import psar_trend
from contigion_indicators.util.functions import get_dataframe_size
import pandas as pd


def test_psar_trend():
    n_candles = 500

    data = pd.read_csv('resources/data.csv')
    sma_data = psar_trend(data)

    assert (get_dataframe_size(sma_data) == (n_candles - 1))
