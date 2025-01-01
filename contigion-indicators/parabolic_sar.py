import pandas as pd
import pandas_ta as ta  # pylint: disable=unused-import
from indicator_utils import indicator_input_validation, indicator_output_validation


def psar_trend(data):
    result = data.copy(deep=True)
    required_columns = ['close']
    min_rows = 0

    indicator_input_validation(data, required_columns, min_rows)

    psar = result.ta.psar()

    indicator_output_validation(psar)

    # Get PSAR values
    result['psar_up'] = psar['PSARs_0.02_0.2']
    result['psar_down'] = psar['PSARl_0.02_0.2']

    # Generate buy/sell signals
    result['signal'] = None
    result.loc[(result['psar_up'].isnull()), 'signal'] = 'buy'
    result.loc[(result['psar_down'].isnull()), 'signal'] = 'sell'

    return result


def ml_psar_trend(data, column_prefix="psar_trend"):
    psar_data = psar_trend(data)
    result = pd.get_dummies(psar_data['signal'], dtype=int, prefix=column_prefix)

    return result
