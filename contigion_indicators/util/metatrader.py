import pandas as pd
from MetaTrader5 import symbol_info, TIMEFRAME_M15, copy_rates_from_pos, initialize # pylint: disable=no-name-in-module


def connect():
    print("Connecting to MT5 ... \n")
    connected = initialize()
    retries = 0

    while not connected:
        print(f"Unable to establish MetaTrader5 connection. Retrying ({retries}) ... \n")
        connected = initialize()

    print("Successfully connected to MetaTrader 5. \n")


def get_point(symbol):
    """
    Retrieves the point value for a given symbol.

    This function attempts to fetch information about the specified symbol
    and extracts its point value. If the symbol information cannot be
    retrieved or an error occurs, an exception is raised.

    Args:
        symbol (str): The trading symbol.

    Returns:
        float: The point value for the symbol.

    Raises:
        RuntimeError: If the symbol information is None.
        Exception: If an error occurs during the retrieval process.
    """

    try:
        info = symbol_info(symbol)

        if info is None:
            raise RuntimeError(f"Failed to retrieve information for symbol: {symbol}")

        return info.point

    except Exception:
        raise Exception("Error retrieving the point value")


def get_market_data(symbol='USDJPY', timeframe=TIMEFRAME_M15, number_of_candles=500):
    """Retrieve market data for a given symbol and timeframe.

    Args:
        symbol (str): The trading symbol.
        timeframe (int): The timeframe value from MetaTrader.
        number_of_candles (int): The number of candles to retrieve.

    Returns:
        DataFrame: A DataFrame containing the market data.

    Raises:
        RuntimeError: If data retrieval fails.
    """
    rates = copy_rates_from_pos(symbol, timeframe, 0, number_of_candles)

    if rates is None:
        raise RuntimeError(f"Failed to retrieve data for {symbol}.")

    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    # Remove the last row if it's an incomplete candle
    if not data.empty:
        data.drop(data.index[-1], inplace=True)

    return data[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
