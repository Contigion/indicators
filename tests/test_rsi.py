import pytest  # pylint: disable=unused-import
import pandas as pd
from contigion_indicators.rsi import rsi, rsi_mavg, rsi_over_bought_sold
from contigion_indicators.util.functions import get_dataframe_size


def test_rsi():
    n_candles = 500
    period = 7

    data = pd.read_csv('data.csv')
    rsi_data = rsi(data, period).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(rsi_data) == (n_candles - period - 1))


def test_rsi_mavg():
    n_candles = 500
    period = 7
    mavg = 14

    data = pd.read_csv('data.csv')
    rsi_data = rsi_mavg(data, period, mavg).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(rsi_data) == (n_candles - mavg - period))


def test_rsi_over_bought_sold():
    n_candles = 500 - 1
    period = 7

    data = pd.read_csv('data.csv')
    rsi_data = rsi_over_bought_sold(data, period).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(rsi_data) == (n_candles - period - 1))
