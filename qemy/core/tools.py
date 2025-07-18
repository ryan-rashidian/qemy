"""Tools and utility functions for Qemy development.."""

import pandas as pd

from qemy.exceptions import DataError


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
