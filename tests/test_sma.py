import pytest
from contigion_indicators.sma import *
from contigion_indicators.util.functions import get_dataframe_size
from contigion_indicators.util.metatrader import get_market_data, connect


def test_sma_crossover():
    n_candles = 500
    fast = 5
    slow = 13

    connect()
    data = get_market_data(number_of_candles=n_candles)
    sma_data = sma_crossover(data, fast, slow).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(sma_data) == (n_candles - slow))


def test_sma_trend():
    n_candles = 500
    period = 200

    connect()
    data = get_market_data(number_of_candles=n_candles)
    sma_data = sma_trend_direction(data, period).drop(columns=['signal']).dropna(inplace=False)

    assert (get_dataframe_size(sma_data) == (n_candles - period))
