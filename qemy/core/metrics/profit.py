"""Profitability Metrics."""

import numpy as np
import pandas as pd

from qemy.core.tools import get_concept_shaped
from qemy.data import EDGARClient, SECFiles


def get_gross_margin(ticker: str, quarters: int=20) -> pd.DataFrame:
    """Derive Gross Margin from filing metrics"""
    df_gross_profit = get_concept_shaped(ticker, 'gprofit', quarters).rename(
        columns={'val': 'val_gprofit'}
    )
    df_revenue = get_concept_shaped(ticker, 'revenue', quarters).rename(
        columns={'val': 'val_rev'}
    )

    df_combined = pd.merge(
        df_gross_profit,
        df_revenue,
        on=['filed', 'form'],
        how='outer'
    ).copy()
    df_combined[['val_gprofit', 'val_rev']] = (
        df_combined[['val_gprofit', 'val_rev']].fillna(0)
    )
    df_combined = df_combined.dropna(subset=['filed'])

    df_combined['val'] = df_combined['val_gprofit'] / df_combined['val_rev']
    df_combined['val'] = df_combined['val'].replace([np.inf, -np.inf], 0)
    df_combined['val'] = df_combined['val'].fillna(0)

    df_combined = df_combined.drop(
        ['val_gprofit', 'val_rev'],
        axis=1
    )

    return df_combined.tail(quarters).reset_index(drop=True)

def ratio_roe(ticker: str) -> dict:
    """Calculate Return on Equity ratio for given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With ticker 'roe' key and corresponding value
    """
    client = EDGARClient(ticker)
    try:
        net_income_concept: SECFiles = client.get_concept(
            concept='netinc'
        )
        net_income_df: pd.DataFrame = net_income_concept.data
        net_income = net_income_df['val'].iloc[-1]
    except Exception:
        net_income = 0.0
    try:
        shareholder_equity_concept: SECFiles = client.get_concept(
            concept='equity'
        )
        shareholder_equity_df: pd.DataFrame = shareholder_equity_concept.data
        ### Calculate shareholder equity 1-year average
        start = shareholder_equity_df['val'].iloc[-4]
        end = shareholder_equity_df['val'].iloc[-1]
        avg_shareholder_equity = (start + end) / 2
    except Exception:
        avg_shareholder_equity = 0.0

    if avg_shareholder_equity <= 0.0:
        return {
            'ticker': ticker,
            'roe': 999999.0
        }

    roe = net_income / avg_shareholder_equity

    return {
        'ticker': ticker,
        'roe': roe
    }

def ratio_roa(ticker: str, quarters: int=10) -> pd.DataFrame:
    """Calculate Return on Assets ratio for given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
    """
    net_income_df = get_concept_shaped(
        ticker = ticker,
        concept = 'netinc',
        quarters = quarters
    ).rename(columns={'val': 'val_netinc'})

    assets_df = get_concept_shaped(
        ticker = ticker,
        concept = 'assets',
        # Add 4 quarters as rolling avgerage buffer
        quarters = quarters + 4
    ).rename(columns={'val': 'val_assets'})
    # Calculate 1-year rolling average
    assets_df['avg_assets'] = assets_df['val_assets'].rolling(window=4).mean()
    assets_df.dropna(inplace=True)
    assets_df = assets_df.tail(quarters).copy()

    df_combined: pd.DataFrame = pd.merge(
        net_income_df,
        assets_df,
        on=['filed', 'form'],
        how='outer',
    ).copy()
    df_combined[[
        'val_netinc', 'avg_assets', 'val_assets'
    ]] = df_combined[[
        'val_netinc', 'avg_assets', 'val_assets'
    ]].fillna(0.0).copy()

    # Avoid dividing by 0
    df_condition = df_combined['avg_assets'] <= 0.0
    # 1e12 denominator gives placeholder '~inf' small val
    df_combined.loc[df_condition, 'avg_assets'] = 1e12

    df_combined['val'] = (
        df_combined['val_netinc'] / df_combined['avg_assets']
    )

    df_roa = df_combined.drop(
        ['val_netinc', 'avg_assets', 'val_assets'],
        axis=1
    )

    return df_roa.tail(quarters).reset_index(drop=True)

def ratio_roic(ticker: str) -> dict:
    """Calculate Return on Invested Capital ratio for given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With ticker 'roic' key and corresponding value
    """
    TAX_RATE = 0.21 # estimate for US corporate tax rate
    client = EDGARClient(ticker)
    try:
        operating_income_concept: SECFiles = client.get_concept(
            concept='opinc'
        )
        operating_income_df: pd.DataFrame = operating_income_concept.data
        operating_income = operating_income_df['val'].iloc[-1]
        # Calculate NOPAT "Net Operating Income After Tax"
        nopat = operating_income * (1.0 - TAX_RATE)
    except Exception:
        nopat = 0.0
    try:
        invested_capital_concept: SECFiles = client.get_concept(
            concept='netcashi'
        )
        invested_capital_df: pd.DataFrame = invested_capital_concept.data
        ### Calculate Invested Capital 1-year average
        start = invested_capital_df['val'].iloc[-4]
        end = invested_capital_df['val'].iloc[-1]
        avg_invested_capital = (start + end) / 2
    except Exception:
        avg_invested_capital = 0.0

    if avg_invested_capital <= 0.0:
        return {
            'ticker': ticker,
            'roic': 999999.0
        }

    roic = nopat / avg_invested_capital

    return {
        'ticker': ticker,
        'roic': roic
    }

def ratio_net_profit_margin():
    return

