import pandas as pd
import pandas_ta as ta  # pylint: disable=unused-import
from indicator_utils import indicator_input_validation, indicator_output_validation
from util.functions import get_dataframe_size


def bollinger_bands(data, period=5, std_dev=2):
    result = data.copy(deep=True)
    required_columns = ['close']
    min_rows = max(period, std_dev)

    indicator_input_validation(data, required_columns, min_rows)

    bbands = result.ta.bbands(length=period, std=std_dev)

    indicator_output_validation(bbands)

    # Assign the Bollinger Bands to the result DataFrame
    result['lower'] = bbands[f"BBL_{period}_{std_dev}.0"]
    result['upper'] = bbands[f"BBU_{period}_{std_dev}.0"]
    result['mavg'] = bbands[f"BBM_{period}_{std_dev}.0"]

    # Generate buy/sell signals
    close_mavg = zip(result['close'], result['mavg'])
    result['signal'] = [
        'buy' if (close > mavg) else
        'sell' if (close < mavg) else
        None
        for close, mavg in close_mavg
    ]

    return result


def ml_bollinger_bands(data, period=5, std_dev=2, column_prefix="bollinger_bands"):
    data_size = get_dataframe_size(data)

    if period > data_size:
        raise ValueError(f"Period ({period}) is greater than the number of rows ({data_size}).")

    bb_data = bollinger_bands(data, period, std_dev)
    result = pd.get_dummies(bb_data['signal'], dtype=int, prefix=column_prefix)

    return result
