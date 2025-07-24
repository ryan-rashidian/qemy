"""Fundamental Metrics."""

from qemy.data import EDGARClient


def ratio_current(ticker: str) -> dict:
    """Calculate Current Ratio of given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With ticker 'current_ratio' key and corresponding value
    """
    client = EDGARClient(ticker)
    try:
        assets_df = client.get_concept(concept='assets')
        assets = assets_df['val'].iloc[-1]
    except Exception:
        assets = 0.0
    try:
        liabilities_df = client.get_concept(concept='liab')
        liabilities = liabilities_df['val'].iloc[-1]
    except Exception:
        liabilities = 0.0

    if liabilities <= 0.0:
        return {
            'ticker': ticker,
            'current_ratio': 999999.0
        }

    current_ratio = assets / liabilities

    return {
        'ticker': ticker,
        'current_ratio': current_ratio
    }

def ratio_quick(ticker: str) -> dict:
    """Calculate Quick Ratio of given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With 'quick_ratio' key and corresponding float value
    """
    client = EDGARClient(ticker)
    try:
        cash_df = client.get_concept(concept='cash')
        cash = cash_df['val'].iloc[-1]
    except Exception:
        cash = 0.0
    try:
        arec_df = client.get_concept(concept='arec')
        arec = arec_df['val'].iloc[-1]
    except Exception:
        arec = 0.0
    try:
        msec_df = client.get_concept(concept='msec')
        msec = msec_df['val'].iloc[-1]
    except Exception:
        msec = 0.0
    try:
        liabilities_df = client.get_concept(concept='liab')
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
        assets_df = client.get_concept(concept='assets')
        assets = assets_df['val'].iloc[-1]
    except Exception:
        assets = 0.0
    try:
        liabilities_df = client.get_concept(concept='liab')
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
        net_income_df = client.get_concept(concept='netinc')
        net_income = net_income_df['val'].iloc[-1]
    except Exception:
        net_income = 0.0
    try:
        revenue_df = client.get_concept(concept='revenue')
        revenue = revenue_df['val'].iloc[-1]
    except Exception:
        revenue = 0.0

    net_margin = (net_income - revenue) / 100

    return {
        'ticker': ticker,
        'net_margin': net_margin
    }

