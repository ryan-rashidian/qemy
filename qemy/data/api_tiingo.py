"""Tiingo API module.

This module requests and fetches data from Tiingo API servers.
"""

import pandas as pd
from qemy import _config as cfg
from qemy.utils.utils_fetch import parse_period, safe_status_get

class TiingoClient:
    """Client for fetching stock market data from Tiingo API."""

    def __init__(self):
        """Initialize TiingoClient with API key and request headers."""
        self.API_KEY: str = cfg.TIINGO_API_KEY
        self.HEADERS: dict[str, str] = {
            'Content-Type': 'application/json',
            'Authorization': f"Token {self.API_KEY}"
        }

    def get_prices(
        self, 
        ticker: str, 
        period: str = '1W', 
        resample = 'daily',             
        columns: str | list[str] = 'adjClose'
    ) -> pd.DataFrame:
        """Fetch historical price data for a given ticker.

        Args:
            ticker (str): Company ticker
            period (str): Period (e.g., "1Y", "3M", "50D")
            resample (str): Resample frequency (e.g., "daily", "weekly")
            columns (str | list[str]): Data columns (e.g. "close", "adjClose")

        Returns:
            pd.DataFrame: DataFrame with pd.DatetimeIndex and column for values  
        """
        start_date, end_date = parse_period(period)

        url = f"{cfg.TIINGO_URL}{ticker}/prices"
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'resampleFreq': resample,
            'columns': columns
        }

        price_data = safe_status_get(
            url=url, 
            headers=self.HEADERS, 
            params=params
        )

        if not price_data:
            return pd.DataFrame()

        # DataFrame formatting step
        price_df = pd.DataFrame(price_data)
        price_df['date'] = pd.to_datetime(price_df['date'])
        price_df.set_index('date', inplace=True)
        price_df.index = pd.DatetimeIndex(price_df.index)

        return price_df if not price_df.empty else pd.DataFrame() 

    def get_quote(self, tickers: str | list[str]) -> dict[str, dict]:
        """Fetch latest quote data for one or more tickers.

        Args:
            tickers (str | list[str]): A single ticker or list of tickers

        Returns:
            dict[str, dict]: With tickers mapped to their quote data
        """
        # Normalize tickers arg to list
        if isinstance(tickers, str):
            tickers = [tickers]

        url = f"{cfg.TIINGO_IEX_URL}{','.join(tickers)}"
        response = safe_status_get(url=url, headers=self.HEADERS)
        if not isinstance(response, list):
            return {}

        return {entry["ticker"]: entry for entry in response if "ticker" in entry}

