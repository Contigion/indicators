import pandas as pd
from util.functions import get_dataframe_size


def indicator_input_validation(data, required_columns, min_rows):
    """
    Validates the input DataFrame to ensure it meets the required conditions.

    Parameters:
    - data: A pandas DataFrame containing the dataset to be validated.
    - required_columns: A list of column names that must be present in the DataFrame.
    - min_rows: The minimum number of rows required in the DataFrame.

    Raises:
    - ValueError: If the DataFrame is empty.
    - ValueError: If the DataFrame does not contain any of the required columns.
    - ValueError: If the number of rows in the DataFrame is less than 'min_rows'.
    """

    data_size = get_dataframe_size(data)

    # Check if data is None
    if data is None:
        raise ValueError("The input DataFrame is empty.")

    # Check for the presence of each required column
    for column in required_columns:
        if column not in data.columns:
            raise ValueError(
                f"There are missing required columns in the DataFrame. Missing column: {column}.")

    # Check if the DataFrame has at least the minimum number of rows
    if not data_size > min_rows:
        raise ValueError(
            f"There aren't enough rows in the input DataFrame. Expected at least {min_rows}, got {data_size}.")


def indicator_output_validation(data):
    """
    Validates the result of an indicator calculation to ensure it is not None and meets basic requirements.

    Parameters:
    - data: The result of the indicator calculation, typically a DataFrame or Series.

    Raises:
    - RuntimeError: If the indicator calculation fails, providing guidance on potential issues.
    """

    # Check if data is None
    if data is None:
        raise RuntimeError(
            "Indicator calculation failed. "
            "Ensure the 'pandas_ta' library is installed and properly configured, "
            "and that the input data meets the necessary requirements for the calculation."
        )

    # Check if data is empty
    if isinstance(data, (pd.DataFrame, pd.Series)) and data.empty:
        raise RuntimeError(
            "Indicator calculation resulted in an empty DataFrame/Series. "
            "Please verify that the input data is valid and suitable for the indicator computation."
        )
