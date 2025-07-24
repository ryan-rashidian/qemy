"""Profitability Metrics."""

from qemy.data import EDGARClient


def ratio_roe(ticker: str) -> dict:
    """Calculate Return on Equity ratio for given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With ticker 'roe' key and corresponding value
    """
    client = EDGARClient(ticker)
    try:
        net_income_df = client.get_concept(concept='netinc')
        net_income = net_income_df['val'].iloc[-1]
    except Exception:
        net_income = 0.0
    try:
        shareholder_equity_df = client.get_concept(concept='equity')
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

def ratio_roa(ticker: str) -> dict:
    """Calculate Return on Assets ratio for given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With ticker 'roa' key and corresponding value
    """
    client = EDGARClient(ticker)
    try:
        net_income_df = client.get_concept(concept='netinc')
        net_income = net_income_df['val'].iloc[-1]
    except Exception:
        net_income = 0.0
    try:
        assets_df = client.get_concept(concept='assets')
        ### Calculate assets 1-year average
        start = assets_df['val'].iloc[-4]
        end = assets_df['val'].iloc[-1]
        avg_assets = (start + end) / 2
    except Exception:
        avg_assets = 0.0

    if avg_assets <= 0.0:
        return {
            'ticker': ticker,
            'roa': 999999.0
        }

    roa = net_income / avg_assets

    return {
        'ticker': ticker,
        'roe': roa
    }

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
        operating_income_df = client.get_concept(concept='opinc')
        operating_income = operating_income_df['val'].iloc[-1]
        # Calculate NOPAT "Net Operating Income After Tax"
        nopat = operating_income * (1.0 - TAX_RATE)
    except Exception:
        nopat = 0.0
    try:
        invested_capital_df = client.get_concept(concept='netcashi')
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

