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


def validate_input(data, required_columns=[], minimum_input=[]):
    data_size = get_dataframe_size(data)

    # Check if data is None
    if data is None:
        raise ValueError("The input DataFrame is None.")

    # Check for the presence of each required column
    for column in required_columns:
        if column not in data.columns:
            raise ValueError(
                f"There are missing required columns in the DataFrame. Missing column: {column}.")

    # Check if the DataFrame has at least the minimum number of rows
    if minimum_input:
        minimum_rows = max(minimum_input)
        if minimum_rows > data_size:
            raise ValueError(
                f"There aren't enough rows in the input DataFrame. Expected at least {minimum_rows}, got {data_size}.")


def validate_output(data):
    if data is None:
        raise ValueError("The output DataFrame is None.")
