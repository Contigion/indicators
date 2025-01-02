import pytest  # pylint: disable=unused-import
from contigion_indicators.bollinger_bands import *
from contigion_indicators.util.functions import get_dataframe_size
from contigion_indicators.util.metatrader import get_market_data, connect


def test_bollinger_bands():
    n_candles = 500
    period = 7

    connect()
    data = get_market_data(number_of_candles=n_candles)
    bb_data = bollinger_bands(data, period).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(bb_data) == (n_candles - period))
