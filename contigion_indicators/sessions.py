from datetime import time
from numpy import where

# Sessions
# USES SA TIME
# Source: https://www.babypips.com/learn/forex/forex-trading-sessions
# and https://www.xm.com/education/chapter-1/trading-sessions
SYDNEY_OPEN = time(0, 00)
SYDNEY_CLOSE = time(8, 00)
TOKYO_OPEN = time(2, 00)
TOKYO_CLOSE = time(10, 00)
LONDON_OPEN = time(9, 00)
LONDON_CLOSE = time(18, 00)
NEW_YORK_OPEN = time(15, 00)
NEW_YORK_CLOSE = time(23, 00)

SESSIONS = ['sydney_session', 'tokyo_session', 'london_session', 'new_york_session']
WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


def trading_session(data):
    result = data.copy(deep=True)
    result['hour'] = result['time'].dt.time

    result[SESSIONS] = 0
    result.loc[(result.hour > SYDNEY_OPEN) & (result.hour < SYDNEY_CLOSE), 'sydney_session'] = 1
    result.loc[(result.hour > TOKYO_OPEN) & (result.hour < TOKYO_CLOSE), 'tokyo_session'] = 1
    result.loc[(result.hour > LONDON_OPEN) & (result.hour < LONDON_CLOSE), 'london_session'] = 1
    result.loc[(result.hour > NEW_YORK_OPEN) & (result.hour < NEW_YORK_CLOSE), 'new_york_session'] = 1

    return result


def day_of_the_week(data):
    result = data.copy(deep=True)
    result['weekday'] = result['time'].dt.day_name()

    result[WEEKDAYS] = 0
    result['monday'] = where(result.weekday == 'Monday', 1, 0)
    result['tuesday'] = where(result.weekday == 'Tuesday', 1, 0)
    result['wednesday'] = where(result.weekday == 'Wednesday', 1, 0)
    result['thursday'] = where(result.weekday == 'Thursday', 1, 0)
    result['friday'] = where(result.weekday == 'Friday', 1, 0)

    result.drop(columns=['weekday'], inplace=True)

    return result
