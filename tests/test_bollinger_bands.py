import pytest  # pylint: disable=unused-import
from contigion_indicators.bollinger_bands import bollinger_bands
from contigion_indicators.util.functions import get_dataframe_size
import pandas as pd


def test_bollinger_bands():
    n_candles = 500
    period = 7

    data = pd.read_csv('resources/data.csv')
    bb_data = bollinger_bands(data, period).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(bb_data) == (n_candles - period))
