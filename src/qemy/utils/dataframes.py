"""Utility wrappers for pandas DataFrames in Qemy."""

import pandas as pd


def normalize_financial_df(
    df: pd.DataFrame,
    value_col: str = 'val',
    date_col: str = 'date'
) -> pd.DataFrame:
    """Normalize shape for DataFrames for all Qemy Clients.

    - Converts `date_col` to datetime.date
    - Sorts rows by date
    - Drop NA dates and duplicate frames (if present)
    - Ensures `value_col` is float type
    - Moves `value_col` to the last column
    """
    df = df.copy()

    df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.date
    df.dropna(subset=[date_col], inplace=True)
    df.sort_values(date_col, inplace=True)

    # Handle duplicates if frame exists
    if 'accn' in df.columns:
        df.drop_duplicates('accn', keep='last', inplace=True)

    df.reset_index(drop=True, inplace=True)
    df[value_col] = df[value_col].astype(float)

    # Ensure value column is last
    column_order = [c for c in df.columns if c != value_col] + [value_col]
    df = df.reindex(columns=column_order)

    return df

