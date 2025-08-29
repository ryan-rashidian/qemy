"""Tools and utility functions for Qemy development.."""

import pandas as pd

from qemy.data import EDGARClient, SECFiles
from qemy.exceptions import DataError


def get_concept_shaped(
    ticker: str,
    concept: str,
    quarters: int=10
) -> pd.DataFrame:
    """Get concept dataframe with missing values filled

    Ensures consistent data shape for returns,
    - if given the same 'quarters' arg.

    Args:
        ticker (str): Company ticker symbol
        concept (str): Concept tag/key
        quarters (int): # of quarters to fetch

    Returns:
        pd.DataFrame = With missing fields filled in
    """
    client = EDGARClient(ticker)
    try:
        given_concept: SECFiles = client.get_concept(
            concept = concept,
            quarters = quarters
        )
        concept_df: pd.DataFrame = given_concept.data
        return concept_df

    except Exception:
        return pd.DataFrame({
            'val': [0.0] * quarters,
            'filed': [pd.NaT] * quarters,
            'form': ['N/A'] * quarters
        })

def get_ttm(series: pd.Series) -> float:
    """Trailing twelve months."""
    series.dropna(inplace=True)
    if len(series) < 4:
        raise DataError("Not enough data for calculation")

    return 1.5 # placeholder

def get_cagr(start: float, end: float, years: float) -> float:
    """Compounded annual growth rate."""
    return (end / start) ** (1 / years) - 1

def calc_yoy():
    return

def safe_divide():
    return
