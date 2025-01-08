def candle_size(data, short=0.3, long=0.7):
    result = data.copy(deep=True)

    result['body'] = abs(data['open'] - data['close'])
    result['total_candle'] = abs(data['high'] - data['low'])

    result['signal'] = None
    result.loc[(result['body'] / result['total_candle'] <= short), 'signal'] = 'small'
    result.loc[result['body'] / result['total_candle'] >= long, 'signal'] = 'large'

    # Drop intermediate columns
    result.drop(columns=['body', 'total_candle'], inplace=True)

    return result


def candle_colour(data):
    result = data.copy(deep=True)

    result['signal'] = None
    result.loc[(result.open < result.close), 'signal'] = 'buy'
    result.loc[(result.open > result.close), 'signal'] = 'sell'

    return result


def candle_body_info(data, short=0.3, long=0.7):
    result = data.copy(deep=True)

    result['body'] = abs(result['open'] - result['close'])
    result['upper_wick'] = abs(result['high'] - result[['open', 'close']].max(axis=1))
    result['lower_wick'] = abs(result['low'] - result[['open', 'close']].min(axis=1))
    result['total_candle'] = abs(result['high'] - result['low'])
    data['body_middle'] = abs(data['high'] + data['low']) / 2

    result['body_size'] = result['body'] / result['total_candle']
    result['upper_wick_size'] = result['upper_wick'] / result['total_candle']
    result['lower_wick_size'] = result['lower_wick'] / result['total_candle']

    # All relative to a candle's own wick and body size
    result['long_upper_wick'] = result['upper_wick_size'] >= long
    result['short_upper_wick'] = result['upper_wick_size'] <= short
    result['long_lower_wick'] = result['lower_wick_size'] >= long
    result['short_lower_wick'] = result['lower_wick_size'] <= short
    result['long_body'] = result['body_size'] >= long
    result['short_body'] = result['body_size'] <= short

    # For dual and triple candlestick patterns
    result['body_1'] = result['body'].shift(2)
    result['body_2'] = result['body'].shift(1)
    result['total_candle_1'] = result['total_candle'].shift(2)
    result['total_candle_2'] = result['total_candle'].shift(1)
    data['body_middle_1'] = data['body_middle'].shift(2)
    data['body_middle_2'] = data['body_middle'].shift(1)

    return result
