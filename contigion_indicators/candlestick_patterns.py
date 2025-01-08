from numpy import where
from .sma import sma_trend
from .util import candle_body_info

CANDLESTICK_PATTERNS = ['bull-spinning-top', 'bear-spinning-top', 'bull-marubozu', 'bear-marubozu', 'doji', 'hammer',
                        'hanging-man', 'inverted-hammer', 'shooting-star', 'tweezer-tops', 'tweezer-bottoms',
                        'bullish-harami', 'bearish-harami', 'bullish-engulfing', 'bearish-engulfing', 'morning-star',
                        'evening-star', 'three-white-soldiers', 'three-black-crows', 'three-inside-up',
                        'three-inside-down']


def get_trend(data):
    result = data.copy(deep=True)
    result['trend'] = sma_trend(data)['signal']

    return result['trend']


def candlestick_setup(data):
    result = candle_body_info(data)
    result['trend'] = get_trend(result)
    result['pattern'] = 'unknown'
    result['signal'] = None

    return result


def candlestick_type(data):
    result = candlestick_setup(data)

    # ----- Bullish Spinning top -----
    bull_spinning_top = where((result['body'] / result['total_candle'] <= 0.3) &
                              (result['upper_wick'] / result['total_candle'] > 0.2) &
                              (result['lower_wick'] / result['total_candle'] > 0.2) &
                              (result['trend'] == 'downtrend') &
                              (result['pattern'] == 'unknown'))[0]

    result.loc[bull_spinning_top, 'pattern'] = 'bull-spinning-top'
    result.loc[bull_spinning_top, 'signal'] = 'buy'

    # ----- Bearish Spinning top -----
    bear_spinning_top = where((result['body'] / result['total_candle'] <= 0.3) &
                              (result['upper_wick'] / result['total_candle'] > 0.2) &
                              (result['lower_wick'] / result['total_candle'] > 0.2) &
                              (result['trend'] == 'uptrend') &
                              (result['pattern'] == 'unknown'))[0]

    result.loc[bear_spinning_top, 'pattern'] = 'bear-spinning-top'
    result.loc[bear_spinning_top, 'signal'] = 'sell'

    # ----- White Marubozu -----
    white_marubozu = where((result['open'] == result['low']) &
                           (result['close'] == result['high']) &
                           (result['pattern'] == 'unknown'))[0]

    result.loc[white_marubozu, 'pattern'] = 'bull-marubozu'
    result.loc[white_marubozu, 'signal'] = 'buy'

    # ----- Black Marubozu -----
    black_marubozu = where((result['open'] == result['high']) &
                           (result['close'] == result['low']) &
                           (result['pattern'] == 'unknown'))[0]

    result.loc[black_marubozu, 'pattern'] = 'bear-marubozu'
    result.loc[black_marubozu, 'signal'] = 'sell'

    # ----- Doji -----
    doji = where((result['open'] == result['close']) &
                 (result['pattern'] == 'unknown'))[0]

    result.loc[doji, 'pattern'] = 'doji'
    result.loc[doji, 'signal'] = 'sell'

    return result


def single_candlestick_pattern(data):
    result = candlestick_setup(data)

    # ----- Hammer -----
    hammer = where((result[['upper_wick', 'lower_wick']].max(axis=1) > result['body'] * 2) &
                   (result['upper_wick'] / result['total_candle'] < 0.05) &
                   (result[['open', 'close']].min(axis=1) > result['body_middle']) &
                   (result['trend'] == 'downtrend') &
                   (result['pattern'] == 'unknown'))[0]

    result.loc[hammer, 'pattern'] = 'hammer'
    result.loc[hammer, 'signal'] = 'buy'

    # ----- Hanging man -----
    hanging_man = where((result['lower_wick'] > result['body'] * 2) &
                        (result['upper_wick'] / result['total_candle'] < 0.05) &
                        (result[['open', 'close']].min(axis=1) > result['body_middle']) &
                        (result['trend'] == 'uptrend') &
                        (result['pattern'] == 'unknown'))[0]

    result.loc[hanging_man, 'pattern'] = 'hanging-man'
    result.loc[hanging_man, 'signal'] = 'sell'

    # ----- Inverted hammer -----
    inverted_hammer = where((result['upper_wick'] > 2 * result['body']) &
                            (result['lower_wick'] / result['total_candle'] < 0.05) &
                            (result[['open', 'close']].max(axis=1) < result['body_middle']) &
                            (result['trend'] == 'downtrend') &
                            (result['pattern'] == 'unknown'))[0]

    result.loc[inverted_hammer, 'pattern'] = 'inverted-hammer'
    result.loc[inverted_hammer, 'signal'] = 'buy'

    # ----- Shooting star -----
    shooting_star = where((result['upper_wick'] > 2 * result['body']) &
                          (result['lower_wick'] / result['total_candle'] < 0.05) &
                          (result[['open', 'close']].max(axis=1) < result['body_middle']) &
                          (result['trend'] == 'uptrend') &
                          (result['pattern'] == 'unknown'))[0]

    result.loc[shooting_star, 'pattern'] = 'shooting-star'
    result.loc[shooting_star, 'signal'] = 'sell'

    return result


def dual_candlestick_pattern(data):
    result = candlestick_setup(data)

    # ----- Bullish engulfing -----
    bullish_engulfing = where((result['trend'] == 'downtrend') &
                              (result['open_1'] > result['close_1']) &
                              (result['open'] < result['close']) &
                              (result['close'] > result['open_1']) &
                              (result['open'] < result['close_1']) &
                              (result['pattern'] == 'unknown'))[0]

    result.loc[bullish_engulfing, 'pattern'] = 'bullish-engulfing'
    result.loc[bullish_engulfing, 'signal'] = 'buy'

    # ----- Bearish engulfing -----
    bearish_engulfing = where((result['trend'] == 'uptrend') &
                              (result['open_1'] < result['close_1']) &
                              (result['open'] > result['close']) &
                              (result['close'] < result['open_1']) &
                              (result['open'] > result['close_1']) &
                              (result['pattern'] == 'unknown'))[0]

    result.loc[bearish_engulfing, 'pattern'] = 'bearish-engulfing'
    result.loc[bearish_engulfing, 'signal'] = 'sell'

    # ----- Bullish harami -----
    bullish_harami = where((result['trend'] == 'downtrend') &
                           (result['open_1'] > result['close_1']) &
                           (result['open'] < result['close']) &
                           (result['close'] < result['open_1']) &
                           (result['open'] > result['close_1']) &
                           (result['pattern'] == 'unknown'))[0]

    result.loc[bullish_harami, 'pattern'] = 'bullish-harami'
    result.loc[bullish_harami, 'signal'] = 'buy'

    # ----- Bearish harami -----
    bearish_harami = where((result['trend'] == 'uptrend') &
                           (result['open_1'] < result['close_1']) &
                           (result['open'] > result['close']) &
                           (result['close'] > result['open_1']) &
                           (result['open'] < result['close_1']) &
                           (result['pattern'] == 'unknown'))[0]

    result.loc[bearish_harami, 'pattern'] = 'bearish-harami'
    result.loc[bearish_harami, 'signal'] = 'sell'

    # ----- Tweezer tops -----
    tweezer_tops = where((result['trend'] == 'uptrend') &
                         (result['open_1'] < result['close_1']) &
                         (result['open'] > result['close']) &
                         (result['high_1'] == result['high']) &
                         (result['pattern'] == 'unknown'))[0]

    result.loc[tweezer_tops, 'pattern'] = 'tweezer-tops'
    result.loc[tweezer_tops, 'signal'] = 'sell'

    # ----- Tweezer bottoms -----
    tweezer_bottoms = where((result['trend'] == 'downtrend') &
                            (result['open_1'] > result['close_1']) &
                            (result['open'] < result['close']) &
                            (result['low_1'] == result['low']) &
                            (result['pattern'] == 'unknown'))[0]

    result.loc[tweezer_bottoms, 'pattern'] = 'tweezer-bottoms'
    result.loc[tweezer_bottoms, 'signal'] = 'buy'

    return result


def triple_candlestick_pattern(data):
    result = candlestick_setup(data)

    # ----- Morning star -----
    morning_star = where((result['trend'] == 'downtrend') &
                         (result['body_1'] / result['total_candle_1'] >= 0.6) &
                         (result['total_candle_2'] < result[['total_candle_1', 'total_candle']].max(axis=1) * 0.6) &
                         (result['open_1'] > result['close_1']) &
                         (result['close'] > result['body_middle_1']) &
                         (result['pattern'] == 'unknown'))[0]

    result.loc[morning_star, 'pattern'] = 'morning-star'
    result.loc[morning_star, 'signal'] = 'buy'

    # ----- Evening star -----
    evening_star = where((result['trend'] == 'uptrend') &
                         (result['body_1'] / result['total_candle_1'] >= 0.6) &
                         (result['total_candle_2'] < result[['total_candle_1', 'total_candle']].max(axis=1) * 0.6) &
                         (result['open_1'] < result['close_1']) &
                         (result['close'] < result['body_middle_1']) &
                         (result['pattern'] == 'unknown'))[0]

    result.loc[evening_star, 'pattern'] = 'evening-star'
    result.loc[evening_star, 'signal'] = 'sell'

    # ----- White soldier -----
    three_white_soldiers = where((result['body_2'] > result['body_1']) &
                                 (result['body'] / result['total_candle'] >= 0.5) &
                                 (result['total_candle'] >= result['body_2']) &
                                 (result['open_1'] < result['close_1']) &
                                 (result['open_2'] < result['close_2']) &
                                 (result['open'] < result['close']) &
                                 (abs(result['close_2'] - result['high_2']) / result['total_candle_2'] < 0.5) &
                                 (result['pattern'] == 'unknown'))[0]

    result.loc[three_white_soldiers, 'pattern'] = 'three-white-soldiers'
    result.loc[three_white_soldiers, 'signal'] = 'buy'

    # ----- Black crow -----
    three_black_crows = where((result['body_2'] > result['body_1']) &
                              (result['body'] / result['total_candle'] >= 0.8) &
                              (result['total_candle'] >= result['body_2']) &
                              (result['open_1'] > result['close_1']) &
                              (result['open_2'] > result['close_2']) &
                              (result['open'] > result['close']) &
                              (abs(result['close_2'] - result['low_2']) / result['total_candle_2'] < 0.3) &
                              (result['pattern'] == 'unknown'))[0]

    result.loc[three_black_crows, 'pattern'] = 'three-black-crows'
    result.loc[three_black_crows, 'signal'] = 'sell'

    # ----- Three inside up -----
    three_inside_up = where((result['trend'] == 'downtrend') &
                            (result['open_1'] > result['close_1']) &
                            (result['close_2'] >= result['body_middle_1']) &
                            (result['close'] > result['high_1']) &
                            (result['pattern'] == 'unknown'))[0]

    result.loc[three_inside_up, 'pattern'] = 'three-inside-up'
    result.loc[three_inside_up, 'signal'] = 'buy'

    # ----- Three inside down -----
    three_inside_down = where((result['trend'] == 'uptrend') &
                              (result['open_1'] < result['close_1']) &
                              (result['close_2'] <= result['body_middle_1']) &
                              (result['close'] < result['low_1']) &
                              (result['pattern'] == 'unknown'))[0]

    result.loc[three_inside_down, 'pattern'] = 'three-inside-down'
    result.loc[three_inside_down, 'signal'] = 'sell'

    return result
