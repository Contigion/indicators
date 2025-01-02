import os
import pandas as pd
import pytest  # pylint: disable=unused-import
from contigion_indicators.macd import macd_crossover
from contigion_indicators.util.functions import get_dataframe_size

current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "resources", "data.csv")


def test_maccd_crossover():
    n_candles = 500
    fast = 12
    slow = 26
    signal = 9

    data = pd.read_csv(csv_path)
    macd_data = macd_crossover(data, fast, slow, signal).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(macd_data) == (n_candles - slow - signal + 1))
