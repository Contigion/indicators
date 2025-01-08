import pandas_ta as ta  # pylint: disable=unused-import
from contigion_indicators.util.functions import validate_input, validate_output


def psar(data):
    required_columns = ['close']
    validate_input(data, required_columns, [])

    result = data.copy(deep=True)
    result[['psar_up', 'psar_down']] = result.ta.psar()[['PSARs_0.02_0.2', 'PSARl_0.02_0.2']]

    validate_output(result)
    return result


def psar_trend(data):
    result = psar(data)

    # Generate buy/sell signals
    result['signal'] = None
    result.loc[(result['psar_up'].isnull()), 'signal'] = 'buy'
    result.loc[(result['psar_down'].isnull()), 'signal'] = 'sell'

    validate_output(result)

    return result
