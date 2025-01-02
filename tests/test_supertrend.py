import os
import pytest  # pylint: disable=unused-import
import pandas as pd
from contigion_indicators.supertrend import supertrend, supertrend_direction
from contigion_indicators.util.functions import get_dataframe_size

current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "resources", "data.csv")


def test_supertrend():
    n_candles = 500
    atr_length = 7
    multiplier = 3
    offset = 0

    data = pd.read_csv(csv_path)
    supertrend_data = supertrend(data, atr_length, multiplier, offset).dropna(inplace=False)

    assert (get_dataframe_size(supertrend_data) == (n_candles - atr_length - 1))


def test_supertrend_direction():
    n_candles = 500
    atr_length = 7
    multiplier = 3
    offset = 0

    data = pd.read_csv(csv_path)
    supertrend_data = supertrend_direction(data, atr_length, multiplier, offset).drop(columns=['signal']).dropna(
        inplace=False)

    assert (get_dataframe_size(supertrend_data) == (n_candles - atr_length - 1))
