from numpy import where
from pandas import get_dummies, concat
from .sma import sma_trend_direction

CANDLESTICK_PATTERNS = ['bull-spinning-top', 'bear-spinning-top', 'bull-marubozu', 'bear-marubozu', 'doji', 'hammer',
                        'hanging-man', 'inverted-hammer', 'shooting-star', 'tweezer-tops', 'tweezer-bottoms',
                        'bullish-harami',
                        'bearish-harami', 'bullish-engulfing', 'bearish-engulfing', 'morning-star', 'evening-star',
                        'three-white-soldiers', 'three-black-crows', 'three-inside-up', 'three-inside-down']


def candle_colour(data):
    result = data.copy(deep=True)

    result['signal'] = None
    result.loc[(result.open < result.close), 'signal'] = 'buy'
    result.loc[(result.open > result.close), 'signal'] = 'sell'

    return result


def candle_size(data, short=0.3, long=0.7):
    result = data.copy(deep=True)

    result['total_candle'] = abs(data['high'] - data['low'])
    result['body'] = abs(data['open'] - data['close'])

    result['signal'] = None
    result.loc[(result['body'] / result['total_candle'] <= short), 'signal'] = 'small'
    result.loc[result['body'] / result['total_candle'] >= long, 'signal'] = 'large'

    # Drop intermediate columns
    result.drop(columns=['body', 'total_candle'], inplace=True)

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

    return result


def multi_candlestick_info(data):
    result = data.copy(deep=True)

    result[['open_1', 'high_1', 'low_1', 'close_1']] = result[['open', 'high', 'low', 'close']].shift(2)
    result[['open_2', 'high_2', 'low_2', 'close_2']] = result[['open', 'high', 'low', 'close']].shift(1)

    result['body_1'] = abs(result['open_1'] - result['close_1'])
    result['body_2'] = abs(result['open_2'] - result['close_2'])
    result['body'] = abs(result['open'] - result['close'])  # candle 3

    result['total_candle_1'] = abs(result['high_1'] - result['low_1'])
    result['total_candle_2'] = abs(result['high_2'] - result['low_2'])
    result['total_candle'] = abs(result['high'] - result['low'])  # candle 3

    result['body_middle_1'] = abs(result['high_1'] + result['low_1']) / 2

    return result


def candlestick_type(data):
    # Candle and body sizes
    result = candle_body_info(data)

    # Trend direction
    result['trend'] = sma_trend_direction(data)['trend']

    # Output
    result['pattern'] = 'unknown'
    result['signal'] = None

    # ----- Bullish Spinning top -----
    bull_spinning_top = where((result.body / result.total_candle <= 0.3) &
                                 (result.upper_wick / result.total_candle > 0.2) &
                                 (result.lower_wick / result.total_candle > 0.2) &
                                 (result.trend == 'downtrend') &
                                 (result.pattern == 'unknown'))[0]

    result.loc[bull_spinning_top, 'pattern'] = 'bull-spinning-top'
    result.loc[bull_spinning_top, 'signal'] = 'buy'

    # ----- Bearish Spinning top -----
    bear_spinning_top = where((result.body / result.total_candle <= 0.3) &
                                 (result.upper_wick / result.total_candle > 0.2) &
                                 (result.lower_wick / result.total_candle > 0.2) &
                                 (result.trend == 'uptrend') &
                                 (result.pattern == 'unknown'))[0]

    result.loc[bear_spinning_top, 'pattern'] = 'bear-spinning-top'
    result.loc[bear_spinning_top, 'signal'] = 'sell'

    # ----- White Marubozu -----
    white_marubozu = where((result.open == result.low) &
                              (result.close == result.high) &
                              (result.pattern == 'unknown'))[0]

    result.loc[white_marubozu, 'pattern'] = 'bull-marubozu'
    result.loc[white_marubozu, 'signal'] = 'buy'

    # ----- Black Marubozu -----
    black_marubozu = where((result.open == result.high) &
                              (result.close == result.low) &
                              (result.pattern == 'unknown'))[0]

    result.loc[black_marubozu, 'pattern'] = 'bear-marubozu'
    result.loc[black_marubozu, 'signal'] = 'sell'

    # ----- Doji -----
    doji = where((result.open == result.close) &
                    (result.pattern == 'unknown'))[0]

    result.loc[doji, 'pattern'] = 'doji'
    result.loc[doji, 'signal'] = 'sell'

    return result


def single_candlestick_pattern(data):
    # Candle and body sizes
    result = candle_body_info(data)

    # Trend direction
    result['trend'] = sma_trend_direction(result)['trend']

    # Output
    result['pattern'] = 'unknown'
    result['signal'] = None

    # ----- Hammer -----
    hammer = where((result[['upper_wick', 'lower_wick']].max(axis=1) > result.body * 2) &
                      (result.upper_wick / result.total_candle < 0.05) &
                      (result[['open', 'close']].min(axis=1) > result.body_middle) &
                      (result.trend == 'downtrend') &
                      (result.pattern == 'unknown'))[0]

    result.loc[hammer, 'pattern'] = 'hammer'
    result.loc[hammer, 'signal'] = 'buy'

    # ----- Hanging man -----
    hanging_man = where((result.lower_wick > result.body * 2) &
                           (result.upper_wick / result.total_candle < 0.05) &
                           (result[['open', 'close']].min(axis=1) > result.body_middle) &
                           (result.trend == 'uptrend') &
                           (result.pattern == 'unknown'))[0]

    result.loc[hanging_man, 'pattern'] = 'hanging-man'
    result.loc[hanging_man, 'signal'] = 'sell'

    # ----- Inverted hammer -----
    inverted_hammer = where((result.upper_wick > 2 * result.body) &
                               (result.lower_wick / result.total_candle < 0.05) &
                               (result[['open', 'close']].max(axis=1) < result.body_middle) &
                               (result.trend == 'downtrend') &
                               (result.pattern == 'unknown'))[0]

    result.loc[inverted_hammer, 'pattern'] = 'inverted-hammer'
    result.loc[inverted_hammer, 'signal'] = 'buy'

    # ----- Shooting star -----
    shooting_star = where((result.upper_wick > 2 * result.body) &
                             (result.lower_wick / result.total_candle < 0.05) &
                             (result[['open', 'close']].max(axis=1) < result.body_middle) &
                             (result.trend == 'uptrend') &
                             (result.pattern == 'unknown'))[0]

    result.loc[shooting_star, 'pattern'] = 'shooting-star'
    result.loc[shooting_star, 'signal'] = 'sell'

    return result


def dual_candlestick_pattern(data):
    # Candle and body sizes
    result = candle_body_info(data)

    # Candlestick 2 and Candlstick 3 result
    result = multi_candlestick_info(data)

    # Trend direction
    result['trend'] = sma_trend_direction(data)['trend']

    # Signal
    result['pattern'] = 'unknown'
    result['signal'] = None

    # ----- Bullish engulfing -----
    bullish_engulfing = where((result.trend == 'downtrend') &
                                 (result.open_1 > result.close_1) &
                                 (result.open < result.close) &
                                 (result.close > result.open_1) &
                                 (result.open < result.close_1) &
                                 (result.pattern == 'unknown'))[0]

    result.loc[bullish_engulfing, 'pattern'] = 'bullish-engulfing'
    result.loc[bullish_engulfing, 'signal'] = 'buy'

    # ----- Bearish engulfing -----
    bearish_engulfing = where((result.trend == 'uptrend') &
                                 (result.open_1 < result.close_1) &
                                 (result.open > result.close) &
                                 (result.close < result.open_1) &
                                 (result.open > result.close_1) &
                                 (result.pattern == 'unknown'))[0]

    result.loc[bearish_engulfing, 'pattern'] = 'bearish-engulfing'
    result.loc[bearish_engulfing, 'signal'] = 'sell'

    # ----- Bullish harami -----
    bullish_harami = where((result.trend == 'downtrend') &
                              (result.open_1 > result.close_1) &
                              (result.open < result.close) &
                              (result.close < result.open_1) &
                              (result.open > result.close_1) &
                              (result.pattern == 'unknown'))[0]

    result.loc[bullish_harami, 'pattern'] = 'bullish-harami'
    result.loc[bullish_harami, 'signal'] = 'buy'

    # ----- Bearish harami -----
    bearish_harami = where((result.trend == 'uptrend') &
                              (result.open_1 < result.close_1) &
                              (result.open > result.close) &
                              (result.close > result.open_1) &
                              (result.open < result.close_1) &
                              (result.pattern == 'unknown'))[0]

    result.loc[bearish_harami, 'pattern'] = 'bearish-harami'
    result.loc[bearish_harami, 'signal'] = 'sell'

    # ----- Tweezer tops -----
    tweezer_tops = where((result.trend == 'uptrend') &
                            (result.open_1 < result.close_1) &
                            (result.open > result.close) &
                            (result.high_1 == result.high) &
                            (result.pattern == 'unknown'))[0]

    result.loc[tweezer_tops, 'pattern'] = 'tweezer-tops'
    result.loc[tweezer_tops, 'signal'] = 'sell'

    # ----- Tweezer bottoms -----
    tweezer_bottoms = where((result.trend == 'downtrend') &
                               (result.open_1 > result.close_1) &
                               (result.open < result.close) &
                               (result.low_1 == result.low) &
                               (result.pattern == 'unknown'))[0]

    result.loc[tweezer_bottoms, 'pattern'] = 'tweezer-bottoms'
    result.loc[tweezer_bottoms, 'signal'] = 'buy'

    return result


def triple_candlestick_pattern(data):
    # Candlestick 2 and Candlstick 3 result
    result = multi_candlestick_info(data)

    # Trend direction
    result['trend'] = sma_trend_direction(result)['trend']

    # Signal
    result['pattern'] = 'unknown'
    result['signal'] = None

    # Candle and body sizes
    multi_candlestick_info(result)

    # ----- Morning star -----
    morning_star = where((result.trend == 'downtrend') &
                            (result.body_1 / result.total_candle_1 >= 0.6) &
                            (result.total_candle_2 < result[['total_candle_1', 'total_candle']].max(axis=1) * 0.6) &
                            (result.open_1 > result.close_1) &
                            (result.close > result.body_middle_1) &
                            (result.pattern == 'unknown'))[0]

    result.loc[morning_star, 'pattern'] = 'morning-star'
    result.loc[morning_star, 'signal'] = 'buy'

    # ----- Evening star -----
    evening_star = where((result.trend == 'uptrend') &
                            (result.body_1 / result.total_candle_1 >= 0.6) &
                            (result.total_candle_2 < result[['total_candle_1', 'total_candle']].max(axis=1) * 0.6) &
                            (result.open_1 < result.close_1) &
                            (result.close < result.body_middle_1) &
                            (result.pattern == 'unknown'))[0]

    result.loc[evening_star, 'pattern'] = 'evening-star'
    result.loc[evening_star, 'signal'] = 'sell'

    # ----- White soldier -----
    three_white_soldiers = where((result.body_2 > result.body_1) &
                                    (result.body / result.total_candle >= 0.5) &
                                    (result.total_candle >= result.body_2) &
                                    (result.open_1 < result.close_1) &
                                    (result.open_2 < result.close_2) &
                                    (result.open < result.close) &
                                    (abs(result.close_2 - result.high_2) / result.total_candle_2 < 0.5) &
                                    (result.pattern == 'unknown'))[0]

    result.loc[three_white_soldiers, 'pattern'] = 'three-white-soldiers'
    result.loc[three_white_soldiers, 'signal'] = 'buy'

    # ----- Black crow -----
    three_black_crows = where((result.body_2 > result.body_1) &
                                 (result.body / result.total_candle >= 0.8) &
                                 (result.total_candle >= result.body_2) &
                                 (result.open_1 > result.close_1) &
                                 (result.open_2 > result.close_2) &
                                 (result.open > result.close) &
                                 (abs(result.close_2 - result.low_2) / result.total_candle_2 < 0.3) &
                                 (result.pattern == 'unknown'))[0]

    result.loc[three_black_crows, 'pattern'] = 'three-black-crows'
    result.loc[three_black_crows, 'signal'] = 'sell'

    # ----- Three inside up -----
    three_inside_up = where((result.trend == 'downtrend') &
                               (result.open_1 > result.close_1) &
                               (result.close_2 >= result.body_middle_1) &
                               (result.close > result.high_1) &
                               (result.pattern == 'unknown'))[0]

    result.loc[three_inside_up, 'pattern'] = 'three-inside-up'
    result.loc[three_inside_up, 'signal'] = 'buy'

    # ----- Three inside down -----
    three_inside_down = where((result.trend == 'uptrend') &
                                 (result.open_1 < result.close_1) &
                                 (result.close_2 <= result.body_middle_1) &
                                 (result.close < result.low_1) &
                                 (result.pattern == 'unknown'))[0]

    result.loc[three_inside_down, 'pattern'] = 'three-inside-down'
    result.loc[three_inside_down, 'signal'] = 'sell'

    return result


def ml_candle_colour(data, column_prefix="candle_colour"):
    candle_data = candle_colour(data)
    result = get_dummies(candle_data['signal'], dtype=int, prefix=column_prefix)

    return result


def ml_candle_size(data, short=0.3, long=0.7, column_prefix="candle_size"):
    candle_data = candle_size(data, short, long)
    result = get_dummies(candle_data['signal'], dtype=int, prefix=column_prefix)

    return result


def ml_candlestick_pattern(data):
    candlestick_types = get_candlestick_type(candlestick_type(data))
    single_candlesticks = get_candlestick_type(single_candlestick_pattern(data))
    dual_candlesticks = get_candlestick_type(dual_candlestick_pattern(data))
    triple_candlesticks = get_candlestick_type(triple_candlestick_pattern(data))
    result = concat([candlestick_types, single_candlesticks, dual_candlesticks, triple_candlesticks], axis=1)
    result.drop(columns=['unknown'], inplace=True)

    missing_columns = list(set(CANDLESTICK_PATTERNS) - set(result.columns))
    result[missing_columns] = 0

    return result


def get_candlestick_type(data):
    result = get_dummies(data['pattern'], dtype=int)
    return result
