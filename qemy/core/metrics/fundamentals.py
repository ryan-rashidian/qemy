"""Fundamental Metrics."""

import numpy as np
import pandas as pd

from qemy.core.tools import get_concept_shaped
from qemy.data import EDGARClient, SECFiles


def ratio_current(ticker: str, quarters: int=10) -> pd.DataFrame:
    """Calculate Current Ratio of given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With ticker 'current_ratio' key and corresponding value
    """
    assets_df = get_concept_shaped(
        ticker = ticker,
        concept = 'assets',
        quarters = quarters
    ).rename(columns={'val': 'val_assets'})

    liabilities_df = get_concept_shaped(
        ticker = ticker,
        concept = 'liab',
        quarters = quarters
    ).rename(columns={'val': 'val_liab'})

    df_combined = pd.merge(
        assets_df,
        liabilities_df,
        on=['filed', 'form'],
        how='outer'
    ).copy()
    df_combined[[
        'val_assets', 'val_liab'
    ]] = df_combined[[
        'val_assets', 'val_liab'
    ]].fillna(1.0).copy()
    df_combined = df_combined.dropna(subset=['filed'])

    df_combined['val'] = df_combined['val_assets'] / df_combined['val_liab']
    df_combined['val'] = df_combined['val'].replace([np.inf, -np.inf], 0)
    df_combined['val'] = df_combined['val'].fillna(0)

    df_combined = df_combined.drop(
        ['val_assets', 'val_liab'],
        axis=1
    )

    return df_combined.tail(quarters).reset_index(drop=True)

def ratio_quick(ticker: str) -> dict:
    """Calculate Quick Ratio of given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With 'quick_ratio' key and corresponding float value
    """
    client = EDGARClient(ticker)
    try:
        cash_concept: SECFiles = client.get_concept(concept='cash')
        cash_df: pd.DataFrame = cash_concept.data
        cash = cash_df['val'].iloc[-1]
    except Exception:
        cash = 0.0
    try:
        arec_concept: SECFiles = client.get_concept(concept='arec')
        arec_df: pd.DataFrame = arec_concept.data
        arec = arec_df['val'].iloc[-1]
    except Exception:
        arec = 0.0
    try:
        msec_concept: SECFiles = client.get_concept(concept='msec')
        msec_df: pd.DataFrame = msec_concept.data
        msec = msec_df['val'].iloc[-1]
    except Exception:
        msec = 0.0
    try:
        liabilities_concept: SECFiles = client.get_concept(concept='liab')
        liabilities_df: pd.DataFrame = liabilities_concept.data
        liabilities = liabilities_df['val'].iloc[-1]
    except Exception:
        liabilities = 0.0

    if liabilities <= 0.0:
        return {
            'ticker': ticker,
            'quick_ratio': 999999.0
        }

    quick_ratio = (cash + arec + msec) / liabilities

    return {
        'ticker': ticker,
        'quick_ratio': quick_ratio
    }

def calc_working_capital(ticker: str) -> dict:
    """Calculate Woking Capital of given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With ticker 'working_capital' key and corresponding value
    """
    client = EDGARClient(ticker)
    try:
        assets_concept: SECFiles = client.get_concept(concept='assets')
        assets_df: pd.DataFrame = assets_concept.data
        assets = assets_df['val'].iloc[-1]
    except Exception:
        assets = 0.0
    try:
        liabilities_concept: SECFiles = client.get_concept(concept='liab')
        liabilities_df = liabilities_concept.data
        liabilities = liabilities_df['val'].iloc[-1]
    except Exception:
        liabilities = 0.0

    working_cap = assets - liabilities

    return {
        'ticker': ticker,
        'working_capital': working_cap
    }

def calc_net_margin(ticker: str) -> dict:
    """Calculate Net Margin of given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With ticker 'net_margin' key and corresponding value
    """
    client = EDGARClient(ticker)
    try:
        net_income_concept: SECFiles = client.get_concept(concept='netinc')
        net_income_df: pd.DataFrame = net_income_concept.data
        net_income = net_income_df['val'].iloc[-1]
    except Exception:
        net_income = 0.0
    try:
        revenue_concept: SECFiles = client.get_concept(concept='revenue')
        revenue_df: pd.DataFrame = revenue_concept.data
        revenue = revenue_df['val'].iloc[-1]
    except Exception:
        revenue = 0.0

    net_margin = (net_income - revenue) / 100

    return {
        'ticker': ticker,
        'net_margin': net_margin
    }

