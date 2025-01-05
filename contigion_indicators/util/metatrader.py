from MetaTrader5 import symbol_info  # pylint: disable=no-name-in-module


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
            raise RuntimeError(f"{__file__}: {get_point.__name__}\n"
                               f"Failed to retrieve information for symbol: {symbol}")

        return info.point

    except Exception:
        raise Exception(f"{__file__}: {get_point.__name__}\n"
                        "Error retrieving the point value")
