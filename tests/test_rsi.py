import pytest  # pylint: disable=unused-import
from contigion_indicators.rsi import rsi_signal, rsi_mavg, rsi_over_bought_sold
from contigion_indicators.util.functions import get_dataframe_size
from .setup import data, n_candles

period = 7
mavg = 14


def test_rsi():
    rsi_data = rsi_signal(data, period).drop(columns=['signal']).dropna(inplace=False)
    assert (get_dataframe_size(rsi_data) == (n_candles - period))


def test_rsi_mavg():
    rsi_data = rsi_mavg(data, period, mavg).drop(columns=['signal']).dropna(inplace=False)
    assert (get_dataframe_size(rsi_data) == (n_candles - mavg - period + 1))


def test_rsi_over_bought_sold():
    rsi_data = rsi_over_bought_sold(data, period).drop(columns=['signal']).dropna(inplace=False)
    assert (get_dataframe_size(rsi_data) == (n_candles - period))
