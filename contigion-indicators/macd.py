import pandas as pd
from util.indicator_utils import indicator_input_validation, indicator_output_validation
from util.functions import get_dataframe_size


def macd_crossover(data, fast=12, slow=26, signal=9):
    result = data.copy(deep=True)
    required_columns = ['close']
    min_rows = max(fast, slow, signal)

    indicator_input_validation(data, required_columns, min_rows)
    macd = result.ta.macd(fast=fast, slow=slow, signal=signal)
    indicator_output_validation(macd)

    result[['macd', 'histogram', 'signal_line']] = macd
    result['prev_signal'] = result['signal_line'].shift(1)
    result['prev_macd'] = result['macd'].shift(1)

    # Generate buy/sell signals
    macd_zip_pairs = zip(result['macd'], result['signal_line'], result['histogram'],
                         result['prev_macd'], result['prev_signal'])

    result['signal'] = [
        'buy' if signal_line < macd < histogram and prev_signal > prev_macd else
        'sell' if histogram < macd < signal_line and prev_signal < prev_macd else
        None
        for macd, signal_line, histogram, prev_macd, prev_signal in macd_zip_pairs
    ]

    # Drop intermediate columns
    result.drop(columns=['prev_signal', 'prev_macd'], inplace=True)

    return result


def ml_macd_crossover(data, fast=12, slow=26, signal=9, column_prefix="macd_crossover"):
    data_size = get_dataframe_size(data)

    if max(fast, slow, signal) > data_size:
        raise ValueError(f"Period ({max(fast, slow, signal)}) is greater than the number of rows ({data_size}).")

    macd_data = macd_crossover(data, fast, slow, signal)
    result = pd.get_dummies(macd_data['signal'], dtype=int, prefix=column_prefix)

    return result
