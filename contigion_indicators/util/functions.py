__all__ = ["get_dataframe_size", "validate_input", "validate_output"]


def get_dataframe_size(dataframe):
    """
    Get the number of rows in a pandas DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame whose size is to be determined.

    Returns:
        int: The number of rows in the DataFrame.
    """

    return dataframe.shape[0]


def validate_input(data, required_columns=None, numeric_fields=None):
    """
    Validates the input DataFrame for required conditions.

    Args:
        data (pd.DataFrame): The input DataFrame to validate.
        required_columns (list, optional): List of column names that must be present in the DataFrame.
        numeric_fields (list, optional): Minimum number of rows expected in the DataFrame.

    Raises:
        ValueError: If the DataFrame is None.
        ValueError: If any required column is missing.
        ValueError: If the DataFrame has fewer rows than the specified minimum.
    """

    data_size = get_dataframe_size(data)

    if data is None:
        raise ValueError(f"{__file__}: {validate_input.__name__}\n"
                         "The input DataFrame cannot be None.")

    if required_columns:
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"{__file__}: {validate_input.__name__}\n"
                             f"There are missing required columns in the DataFrame: {', '.join(missing_columns)}.")

    # Check if the DataFrame has at least the minimum number of rows
    if numeric_fields:
        minimum_rows = max(numeric_fields)
        if minimum_rows > data_size:
            raise ValueError(f"{__file__}: {validate_input.__name__}\n"
                             f"There aren't enough rows in the input DataFrame. "
                             f"Expected at least {minimum_rows}, got {data_size}.")


def validate_output(data):
    """
    Validates the output DataFrame.

    Args:
        data (pd.DataFrame): The output DataFrame to validate.

    Raises:
        ValueError: If the DataFrame is None.
    """
    if data is None:
        raise ValueError(f"{__file__}: {validate_output.__name__}\n"
                         "The output DataFrame cannot be None.")
