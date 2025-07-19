"""Cash Flow Metrics."""

import pandas as pd

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
    client = EDGARClient(ticker)

    def _get_latest_val(concept: str) -> pd.DataFrame:
        try:
            return client.get_concept(concept=concept, quarters=quarters)
        except Exception:
            return pd.DataFrame({
                'val': [0.0] * quarters,
                'filed': [pd.NaT] * quarters,
                'form': ['N/A'] * quarters
            })

    df_debt = _get_latest_val('debt').rename(
        columns={'val': 'val_debt'}
    )
    df_debt_short = _get_latest_val('sdebt').rename(
        columns={'val': 'val_sdebt'}
    )
    df_debt_long = _get_latest_val('ldebt').rename(
        columns={'val': 'val_ldebt'}
    )
    df_cash = _get_latest_val('cash').rename(
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

