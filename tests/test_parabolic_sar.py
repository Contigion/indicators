import os
import pandas as pd
import pytest  # pylint: disable=unused-import
from contigion_indicators.parabolic_sar import psar_trend
from contigion_indicators.util.functions import get_dataframe_size

current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "resources", "data.csv")


def test_psar_trend():
    n_candles = 500

    data = pd.read_csv(csv_path)
    sma_data = psar_trend(data)

    assert (get_dataframe_size(sma_data) == (n_candles - 1))
