import pandas_ta as ta  # pylint: disable=unused-import
from contigion_indicators.util.functions import validate_input, validate_output


def rsi(data, period, mavg=14):
    required_columns = ['close']
    periods = [period, mavg]
    validate_input(data, required_columns, periods)

    result = data.copy(deep=True)
    result['rsi'] = result.ta.rsi(period)

    validate_output(result)
    return result


def rsi_signal(data, period=7, overbought=70, oversold=30):
    result = rsi(data, period)
    result['prev_rsi'] = result['rsi'].shift(1)

    # Generate buy/sell signals
    rsi_zip = zip(result['rsi'], result['prev_rsi'])

    result['signal'] = [
        'buy' if (curr_rsi > oversold > prev_rsi) else
        'sell' if (curr_rsi < overbought < prev_rsi) else
        None
        for curr_rsi, prev_rsi in rsi_zip
    ]

    # Drop intermediate columns
    result.drop(columns=['prev_rsi'], inplace=True)
    validate_output(result)

    return result


def rsi_mavg(data, period=7, mavg=14):
    result = rsi(data, period, mavg)
    result['mavg'] = result['rsi'].rolling(mavg).mean()
    result['prev_mavg'] = result['mavg'].shift(1)
    result['prev_rsi'] = result['rsi'].shift(1)

    # Generate buy/sell signals
    rsi_mavg_zip = zip(result['rsi'], result['prev_rsi'], result['mavg'], result['prev_mavg'])

    result['signal'] = [
        'buy' if (50 > curr_rsi > curr_mavg) and (prev_rsi < prev_mavg) else
        'sell' if (50 < curr_rsi < curr_mavg) and (prev_rsi > prev_mavg) else
        None
        for curr_rsi, prev_rsi, curr_mavg, prev_mavg in rsi_mavg_zip
    ]

    # Drop intermediate columns
    result.drop(columns=['prev_rsi', 'prev_mavg'], inplace=True)
    validate_output(result)

    return result


def rsi_over_bought_sold(data, period=7, overbought=70, oversold=30):
    result = rsi(data, period)

    # Generate buy/sell signals
    result['signal'] = None
    result.loc[(result.rsi < oversold), 'signal'] = 'buy'
    result.loc[(result.rsi > overbought), 'signal'] = 'sell'

    validate_output(result)

    return result
