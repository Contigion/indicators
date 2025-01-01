import pandas as pd
import pandas_ta as ta  # pylint: disable=unused-import
from indicator_utils import indicator_input_validation, indicator_output_validation
from util.functions import get_dataframe_size


def sma_crossover(data, fast=5, slow=13):
    result = data.copy(deep=True)
    required_columns = ['close']
    min_rows = slow

    indicator_input_validation(data, required_columns, min_rows)

    slow_sma = result.ta.sma(slow)
    fast_sma = result.ta.sma(fast)

    indicator_output_validation(slow_sma)
    indicator_output_validation(fast_sma)

    result['sma_slow'] = slow_sma
    result['sma_fast'] = fast_sma
    result['prev_slow'] = result['sma_slow'].shift(1)
    result['prev_fast'] = result['sma_fast'].shift(1)

    # Generate buy/sell signals
    sma_zip = zip(result['sma_slow'], result['sma_fast'], result['prev_slow'], result['prev_fast'])
    result['signal'] = [
        'buy' if (curr_slow > curr_fast) and (prev_slow < prev_fast) else
        'sell' if (curr_slow < curr_fast) and (prev_slow > prev_fast) else
        None
        for curr_slow, curr_fast, prev_slow, prev_fast in sma_zip
    ]

    # Drop intermediate columns
    result.drop(columns=['prev_slow', 'prev_fast'], inplace=True)

    return result


def sma_trend_direction(data, period=200):
    result = data.copy(deep=True)
    required_columns = ['close']
    min_rows = period

    indicator_input_validation(data, required_columns, min_rows)

    sma = result.ta.sma(period)

    indicator_output_validation(sma)

    # Add SMAs
    result['sma'] = sma

    # Generate buy/sell signals
    result['trend_direction'] = None
    result.loc[(result.close > result.sma), 'trend_direction'] = 'buy'
    result.loc[(result.close < result.sma), 'trend_direction'] = 'sell'

    result['trend'] = result['trend_direction'].shift(1)

    # Drop intermediate columns
    result.drop(columns=['trend_direction'], inplace=True)

    return result


def ml_sma_crossover(data, fast=5, slow=13, column_prefix="sma_crossover"):
    data_size = get_dataframe_size(data)

    if max(fast, slow) > data_size:
        raise ValueError(f"Period ({max(fast, slow)}) is greater than the number of rows ({data_size}).")

    sma_data = sma_crossover(data, fast, slow)
    result = pd.get_dummies(sma_data['signal'], dtype=int, prefix=column_prefix)

    return result


def ml_sma_trend_direction(data, period=200, column_prefix="sma_trend"):
    data_size = get_dataframe_size(data)

    if period > data_size:
        raise ValueError(f"Period ({period}) is greater than the number of rows ({data_size}).")

    sma_data = sma_trend_direction(data, period)
    result = pd.get_dummies(sma_data['trend'], dtype=int, prefix=column_prefix)

    return result
