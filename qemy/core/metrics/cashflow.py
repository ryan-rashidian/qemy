"""Cash Flow Metrics."""

import pandas as pd

from qemy.data import EDGARClient


def get_fcf(ticker: str, quarters: int=20) -> pd.DataFrame:
    """Derive Free Cash Flow from filing metrics."""
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

def get_netdebt(ticker: str) -> float:
    """Derive Net Debt from filing metrics."""
    client = EDGARClient(ticker)

    def _get_latest_val(concept: str) -> float:
        try:
            df = client.get_concept(concept=concept)
            return df['val'].iloc[-1]
        except Exception:
            return 0.0

    debt = _get_latest_val('debt')
    debt_short = _get_latest_val('sdebt')
    debt_long = _get_latest_val('ldebt')
    cash = _get_latest_val('cash')

    return (debt + debt_short + debt_long) - cash

