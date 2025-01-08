import pandas_ta as ta  # pylint: disable=unused-import
from contigion_indicators.util.functions import validate_input, validate_output


def get_supertrend_data(data, atr_length, multiplier, offset):
    required_columns = ['close']
    periods = [atr_length, multiplier, offset]
    validate_input(data, required_columns, periods)

    result = data.copy(deep=True)
    supertrend_column = f'SUPERT_{atr_length}_{multiplier}.{offset}'
    supertrend_data = result.ta.supertrend(atr_length, multiplier, offset)

    result['supertrend'] = supertrend_data[supertrend_column]
    result.loc[0, 'supertrend'] = None

    validate_output(result)
    return result


def supertrend(data, atr_length=7, multiplier=3, offset=0):
    result = get_supertrend_data(data, atr_length, multiplier, offset)
    validate_output(result)

    return result


def supertrend_trend(data, atr_length=7, multiplier=3, offset=0):
    result = get_supertrend_data(data, atr_length, multiplier, offset)

    # Generate buy/sell signals
    result['signal'] = None
    result.loc[(result['close'] > result['supertrend']), 'signal'] = 'buy'
    result.loc[(result['close'] < result['supertrend']), 'signal'] = 'sell'

    validate_output(result)

    return result
