import pandas_ta as ta  # pylint: disable=unused-import
from contigion_indicators.util.functions import validate_input, validate_output


def get_bb_data(data, period, std_dev):
    required_columns = ['close']
    periods = [period]
    validate_input(data, required_columns, periods)

    result = data.copy(deep=True)
    bbands = result.ta.bbands(length=period, std=std_dev)

    # Assign the Bollinger Bands to the result DataFrame
    result['lower'] = bbands[f"BBL_{period}_{std_dev}.0"]
    result['upper'] = bbands[f"BBU_{period}_{std_dev}.0"]
    result['mavg'] = bbands[f"BBM_{period}_{std_dev}.0"]

    validate_output(result)

    return result


def bollinger_bands(data, period=5, std_dev=2):
    result = get_bb_data(data, period, std_dev)

    # Generate buy / sell signals
    close_mavg = zip(result['close'], result['mavg'])
    result['signal'] = [
        'buy' if (close > mavg) else
        'sell' if (close < mavg) else
        None
        for close, mavg in close_mavg
    ]

    validate_output(result)

    return result
