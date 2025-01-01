import pandas as pd
from util.indicator_utils import indicator_input_validation, indicator_output_validation
from util.functions import get_dataframe_size


def get_rsi_data(data, period):
    result = data.copy(deep=True)
    required_columns = ['close']
    min_rows = period

    indicator_input_validation(data, required_columns, min_rows)
    rsi_data = result.ta.rsi(period)
    indicator_output_validation(rsi_data)
    result['rsi'] = rsi_data

    return result


def rsi(data, period=7, overbought=70, oversold=30):
    result = get_rsi_data(data, period)
    result['prev_rsi'] = result['rsi'].shift(1)

    # Generate buy/sell signals
    rsi_zip = zip(result['rsi'], result['prev_rsi'])

    result['signal'] = [
        'buy' if (curr_rsi > oversold > prev_rsi) else
        'sell' if (curr_rsi < overbought < prev_rsi) else
        None
        for curr_rsi, prev_rsi in rsi_zip
    ]

    # Drop intermediate columns
    result.drop(columns=['prev_rsi'], inplace=True)

    return result


def rsi_over_bought_sold(data, period=7, overbought=70, oversold=30):
    result = get_rsi_data(data, period)

    # Generate buy/sell signals
    result['signal'] = None
    result.loc[(result.rsi < oversold), 'signal'] = 'buy'
    result.loc[(result.rsi > overbought), 'signal'] = 'sell'

    return result


def rsi_mavg(data, period=7, mavg=14):
    result = get_rsi_data(data, period)

    result['prev_rsi'] = result['rsi'].shift(1)
    result['mavg'] = result['rsi'].rolling(mavg).mean()
    result['prev_mavg'] = result['mavg'].shift(1)

    # Generate buy/sell signals
    rsi_mavg_zip = zip(result['rsi'], result['prev_rsi'], result['mavg'], result['prev_mavg'])

    result['signal'] = [
        'buy' if (50 > curr_rsi > curr_mavg) and (prev_rsi < prev_mavg) else
        'sell' if (50 < curr_rsi < curr_mavg) and (prev_rsi > prev_mavg) else
        None
        for curr_rsi, prev_rsi, curr_mavg, prev_mavg in rsi_mavg_zip
    ]

    # Drop intermediate columns
    result.drop(columns=['prev_rsi', 'prev_mavg'], inplace=True)

    return result


def ml_rsi(data, period=7, overbought=70, oversold=30, column_prefix="rsi"):
    data_size = get_dataframe_size(data)

    if period > data_size:
        raise ValueError(f"Period ({period}) is greater than the number of rows ({data_size}).")

    rsi_data = rsi(data, period, overbought, oversold)
    result = pd.get_dummies(rsi_data['signal'], dtype=int, prefix=column_prefix)

    return result


def ml_rsi_over_bought_sold(data, period=7, overbought=70, oversold=30, column_prefix="rsi_over_bought_sold"):
    data_size = get_dataframe_size(data)

    if period > data_size:
        raise ValueError(f"Period ({period}) is greater than the number of rows ({data_size}).")

    rsi_data = rsi_over_bought_sold(data, period, overbought, oversold)
    result = pd.get_dummies(rsi_data['signal'], dtype=int, prefix=column_prefix)

    return result


def ml_rsi_mavg(data, period=7, mavg=14, column_prefix="rsi_mavg"):
    data_size = get_dataframe_size(data)

    if max(period, mavg) > data_size:
        raise ValueError(f"Period ({max(period, mavg)}) is greater than the number of rows ({data_size}).")

    rsi_data = rsi_mavg(data, period, mavg)
    result = pd.get_dummies(rsi_data['signal'], dtype=int, prefix=column_prefix)

    return result
