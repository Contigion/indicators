import pandas_ta as ta  # pylint: disable=unused-import
from .util.functions import validate_input, validate_output


def get_psar_data(data):
    required_columns = ['close']
    validate_input(data, required_columns, [])

    result = data.copy(deep=True)
    psar = result.ta.psar()
    result['psar_up'] = psar['PSARs_0.02_0.2']
    result['psar_down'] = psar['PSARl_0.02_0.2']

    validate_output(result)
    return result


def psar_trend(data):
    result = get_psar_data(data)

    # Generate buy/sell signals
    result['signal'] = None
    result.loc[(result['psar_up'].isnull()), 'signal'] = 'buy'
    result.loc[(result['psar_down'].isnull()), 'signal'] = 'sell'

    validate_output(result)

    return result
