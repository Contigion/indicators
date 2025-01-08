import pandas_ta as ta  # pylint: disable=unused-import
from contigion_indicators.util.functions import validate_input, validate_output


def macd(data, fast, slow, signal):
    required_columns = ['close']
    periods = [slow + signal]
    validate_input(data, required_columns, periods)

    result = data.copy(deep=True)
    result[['macd', 'histogram', 'signal_line']] = result.ta.macd(fast=fast, slow=slow, signal=signal)
    result['prev_signal'] = result['signal_line'].shift(1)
    result['prev_macd'] = result['macd'].shift(1)

    validate_output(result)

    return result


def macd_crossover(data, fast=12, slow=26, signal=9):
    result = macd(data, fast, slow, signal)

    # Generate buy/sell signals
    macd_zip_pairs = zip(result['macd'], result['signal_line'], result['histogram'],
                         result['prev_macd'], result['prev_signal'])

    result['signal'] = [
        'buy' if signal_line < macd_ < histogram and prev_signal > prev_macd else
        'sell' if histogram < macd_ < signal_line and prev_signal < prev_macd else
        None
        for macd_, signal_line, histogram, prev_macd, prev_signal in macd_zip_pairs
    ]

    # Drop intermediate columns
    result.drop(columns=['prev_signal', 'prev_macd'], inplace=True)
    validate_output(result)

    return result
