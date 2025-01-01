import pandas as pd
import pandas_ta as ta  # pylint: disable=unused-import
from indicator_utils import indicator_input_validation, indicator_output_validation
from util.functions import get_dataframe_size


def supertrend(data, atr_length=7, multiplier=3, offset=0):
    result = data.copy(deep=True)
    required_columns = ['close']
    min_rows = max(atr_length, multiplier, offset)

    indicator_input_validation(data, required_columns, min_rows)

    supertrend_column = f"SUPERT_{atr_length}_{multiplier}.{offset}"
    supertrend_data = result.ta.supertrend(atr_length, multiplier, offset)

    indicator_output_validation(supertrend_data)

    result['supertrend'] = supertrend_data[supertrend_column]
    result.loc[0, 'supertrend'] = None

    return result


def supertrend_direction(data, atr_length=7, multiplier=3, offset=0):
    result = data.copy(deep=True)

    result['supertrend'] = supertrend(result, atr_length, multiplier, offset)['supertrend']

    # Generate buy/sell signals
    result['signal'] = None
    result.loc[(result['close'] > result['supertrend']), 'signal'] = 'buy'
    result.loc[(result['close'] < result['supertrend']), 'signal'] = 'sell'

    return result


def ml_supertrend_direction(data, atr_length=7, multiplier=3, offset=0, column_prefix="supertrend"):
    data_size = get_dataframe_size(data)

    if atr_length > data_size:
        raise ValueError(f"ATR Length ({atr_length}) is greater than the number of rows ({data_size}).")

    supertrend_data = supertrend_direction(data, atr_length, multiplier, offset)
    result = pd.get_dummies(supertrend_data['signal'], dtype=int, prefix=column_prefix)

    return result
