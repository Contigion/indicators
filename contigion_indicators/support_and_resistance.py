from numpy import any as np_any, array, newaxis
from contigion_indicators.util.metatrader import get_point


def support_and_resistance(symbol, data, window=2, target=10):
    point = get_point(symbol)
    s_and_r, support, resistance = get_support_and_resistance_levels(data, window)
    close = s_and_r['close'].values
    suport_levels = array(support['level'])
    resistance_levels = array(resistance['level'])

    s_and_r['is_support_close'] = np_any(abs(close[:, newaxis] - suport_levels) < (target * point), axis=1)
    s_and_r['is_resistance_close'] = np_any(abs(close[:, newaxis] - resistance_levels) < (target * point), axis=1)

    return s_and_r


def get_support_and_resistance_levels(data, window=5):
    result = data.copy(deep=True)

    # Get candles within window
    for i in range(1, window + 1):
        result[f"previous_candle_high_{i}"] = result['high'].shift(i)
        result[f"previous_candle_low_{i}"] = result['low'].shift(i)
        result[f"next_candle_high_{i}"] = result['high'].shift(-i)
        result[f"next_candle_low_{i}"] = result['low'].shift(-i)

    # Get valid support indices / levels
    result['is_support'] = (result
                            .filter(regex="previous_candle_low_|next_candle_low_")
                            .ge(result['low'], axis=0)
                            .all(axis=1))

    # Get valid resisitance indices / levels
    result['is_resistance'] = (result
                               .filter(regex="previous_candle_high_|next_candle_high_")
                               .le(result['high'], axis=0)
                               .all(axis=1))

    support = result[result['is_support']].copy(deep=True)
    resistance = result[result['is_resistance']].copy(deep=True)

    broken_support_indices = []
    broken_resistance_indices = []

    # Remove violated levels
    for index, row in support.iterrows():
        next_index = index + 1
        is_level_broken = np_any(result.filter(items=['close']).loc[next_index:] < row.low)

        if is_level_broken:
            broken_support_indices.append(index)

    for index, row in resistance.iterrows():
        next_index = index + 1
        is_level_broken = np_any(result.filter(items=['close']).loc[next_index:] > row.low)

        if is_level_broken:
            broken_resistance_indices.append(index)

    support.drop(broken_support_indices, inplace=True)
    resistance.drop(broken_resistance_indices, inplace=True)
    support['level'] = support['low']
    resistance['level'] = resistance['high']

    # Drop columns
    added_columns = result.filter(regex='previous_candle_low_|next_candle_low_|previous_candle_high_|next_candle_high_')
    result.drop(columns=added_columns.columns, inplace=True)

    return result, support[['time', 'level']], resistance[['time', 'level']]
