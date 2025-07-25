"""Cash Flow Metrics."""

import pandas as pd

from qemy.core.tools import get_concept_shaped
from qemy.data import EDGARClient


def get_fcf(ticker: str, quarters: int=20) -> pd.DataFrame:
    """Derive Free Cash Flow from filing metrics.

    Args:
        ticker (str): Company ticker symbol
        quarters (int): # of quarters to fetch

    Returns:
        pd.DataFrame: With historic FCF data
    """
    client = EDGARClient(ticker)
    df_ocf = client.get_concept(
        concept='ocf',
        quarters=quarters
    )
    df_capex = client.get_concept(
        concept='capex',
        quarters=quarters
    )

    df_cash_combined: pd.DataFrame = pd.merge(
        df_ocf,
        df_capex,
        on=['filed', 'form'],
        how='outer',
        suffixes=('_ocf', '_capex')
    ).copy()
    df_combined = df_cash_combined.fillna(0)
    df_combined['val'] = (
        df_combined['val_ocf'] - df_combined['val_capex']
    )
    df_fcf = df_combined.drop(['val_ocf', 'val_capex'], axis=1)

    return df_fcf.sort_values('filed').tail(quarters)

def get_netdebt(ticker: str, quarters: int=20) -> pd.DataFrame:
    """Derive Net Debt from filing metrics.

    Args:
        ticker (str): Company ticker symbol
        quarters (int): # of quarters to fetch

    Returns:
        pd.DataFrame: With historic Net Debt data
    """
    df_debt = get_concept_shaped(ticker, 'debt', quarters).rename(
        columns={'val': 'val_debt'}
    )
    df_debt_short = get_concept_shaped(ticker, 'sdebt', quarters).rename(
        columns={'val': 'val_sdebt'}
    )
    df_debt_long = get_concept_shaped(ticker, 'ldebt', quarters).rename(
        columns={'val': 'val_ldebt'}
    )
    df_cash = get_concept_shaped(ticker, 'cash', quarters).rename(
        columns={'val': 'val_cash'}
    )

    df_combined: pd.DataFrame = pd.merge(
        df_debt,
        df_debt_short,
        on=['filed', 'form'],
        how='outer',
    ).copy()
    df_combined = pd.merge(
        df_debt_long,
        df_combined,
        on=['filed', 'form'],
        how='outer',
    ).copy()
    df_combined = pd.merge(
        df_cash,
        df_combined,
        on=['filed', 'form'],
        how='outer',
    ).copy()

    # Placeholder 0 for missing values
    # Allows for missing components in quarterly calculations
    df_combined[[
        'val_debt', 'val_sdebt', 'val_ldebt', 'val_cash'
    ]] = df_combined[[
        'val_debt', 'val_sdebt', 'val_ldebt', 'val_cash'
    ]].fillna(0)

    df_combined = df_combined.dropna(subset=['filed'])

    df_combined['val'] = ((df_combined['val_debt']
                    + df_combined['val_sdebt']
                    + df_combined['val_ldebt'])
                    - df_combined['val_cash'])

    df_netdebt = df_combined.drop(
        ['val_debt', 'val_sdebt', 'val_ldebt', 'val_cash'],
        axis=1
    )

    return df_netdebt.tail(quarters).reset_index(drop=True)

