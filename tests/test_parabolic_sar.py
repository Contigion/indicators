import pytest
from contigion_indicators.parabolic_sar import *
from contigion_indicators.util.functions import get_dataframe_size
from contigion_indicators.util.metatrader import get_market_data, connect


def test_psar_trend():
    n_candles = 500

    connect()
    data = get_market_data(number_of_candles=n_candles)
    sma_data = psar_trend(data)

    assert (get_dataframe_size(sma_data) == (n_candles - 1))