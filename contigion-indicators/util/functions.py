def get_dataframe_size(dataframe):
    """
    Get the number of rows in a pandas DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame whose size is to be determined.

    Returns:
        int: The number of rows in the DataFrame.
    """

    return dataframe.shape[0]
