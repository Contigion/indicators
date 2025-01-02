import pytest  # pylint: disable=unused-import
from contigion_indicators.sma import sma_crossover, sma_trend_direction
from contigion_indicators.util.functions import get_dataframe_size
import pandas as pd
import os

current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "resources", "data.csv")


def test_sma_crossover():
    n_candles = 500
    fast = 5
    slow = 13

    data = pd.read_csv(csv_path)
    sma_data = sma_crossover(data, fast, slow).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(sma_data) == (n_candles - slow))


def test_sma_trend():
    n_candles = 500
    period = 200

    data = pd.read_csv(csv_path)
    sma_data = sma_trend_direction(data, period).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(sma_data) == (n_candles - period))
