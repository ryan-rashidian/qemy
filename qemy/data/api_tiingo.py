"""Tiingo API module.

This module requests and fetches data from Tiingo API.
"""
from __future__ import annotations

import logging

import pandas as pd

from qemy import _config as cfg

from ._api_tools import ClientError, parse_period, safe_status_get

logger = logging.getLogger(__name__)

class TiingoClient:
    """Client for fetching stock market data from Tiingo API."""

    def __init__(self, ticker: str | list[str]):
        """Initialize TiingoClient with API key and request headers.

        Args:
            ticker (str | list[str]): Company ticker symbol(s)

        Raises:
            ClientError: If self.tickers cannot be defined
        """
        self.tickers = self._normalize_tickers(ticker)
        self.ticker = self.tickers[0]

        self.API_KEY: str = cfg.tiingo_api_key()
        self.HEADERS: dict[str, str] = {
            'Content-Type': 'application/json',
            'Authorization': f"Token {self.API_KEY}"
        }

    def _normalize_tickers(
        self,
        ticker: str | list[str] | object
    ) -> list[str]:
        """Internal method for normalizing ticker argument.

        Args:
            ticker (str | list[str] | object): Company ticker symbol(s)

        Returns:
            list[str]: Normalized ticker list for self.tickers

        Raises:
            ClientError: If ticker argument is invalid type
        """
        if isinstance(ticker, str):
            if not ticker:
                raise ClientError("Args (ticker): empty string")
            return [ticker.strip().upper()]

        elif isinstance(ticker, list):
            if not ticker:
                raise ClientError("Args (ticker): empty list")

            normalized_tickers = []

            for i, t in enumerate(ticker):
                if not isinstance(t, str):
                    raise ClientError(
                        f"Args (ticker[{i}]): incorrect type: {type(t)}"
                    )

                clean_ticker = t.strip().upper()
                if not clean_ticker:
                    raise ClientError(f"Args (ticker[{i}]): empty string")
                normalized_tickers.append(clean_ticker)

            return normalized_tickers

        else:
            logger.error(f"Failed to initialize agument: {ticker}")
            raise ClientError(
                f"Args (ticker): incorrect type: {type(ticker)}"
            )

    def __repr__(self) -> str:
        return f"TiingoClient(ticker={self.tickers})"

    def __str__(self) -> str:
        return f"[TiingoClient]\nticker={self.tickers}"

    def __bool__(self) -> bool:
        return bool(self.tickers)

    def __len__(self) -> int:
        return len(self.tickers)

    def __getitem__(self, position) -> str:
        return self.tickers[position]

    def __add__(self, other) -> TiingoClient:
        new_tickers = self.tickers.copy()
        for t in self._normalize_tickers(other):
            if t not in new_tickers:
                new_tickers.append(t)
        return TiingoClient(new_tickers)

    def __sub__(self, other) -> TiingoClient:
        remove = set(self._normalize_tickers(other))
        new_tickers = [t for t in self.tickers if t not in remove]
        return TiingoClient(new_tickers)

    def __iadd__(self, other) -> TiingoClient:
        for t in self._normalize_tickers(other):
            if t not in self.tickers:
                self.tickers.append(t)
        return self

    def __isub__(self, other) -> TiingoClient:
        remove = set(self._normalize_tickers(other))
        self.tickers = [t for t in self.tickers if t not in remove]
        return self

    def get_prices(
        self,
        period: str = '1W',
        resample: str = 'daily',
        columns: str | list[str] = 'adjClose'
    ) -> pd.DataFrame:
        """Fetch historical price data for a given ticker.

        This module will only return data for the first[0] ticker string.

        Args:
            period (str): Period (e.g., "1Y", "3M", "50D")
            resample (str): Resample frequency (e.g., "daily", "weekly")
            columns (str | list[str]): Data columns (e.g. "close", "adjClose")

        Returns:
            pd.DataFrame: DataFrame with pd.DatetimeIndex and column for values
        """
        start_date, end_date = parse_period(period)

        url = f"{cfg.TIINGO_URL}{self.ticker}/prices"
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
            logger.error("Tiingo API request Failed")
            return pd.DataFrame()
        logger.info("Tiingo API request Successful")

        price_df = pd.DataFrame(price_data)
        price_df['date'] = pd.to_datetime(price_df['date'])
        price_df.set_index('date', inplace=True)
        price_df.index = pd.DatetimeIndex(price_df.index)

        return price_df if not price_df.empty else pd.DataFrame()

    def get_quote(self) -> dict[str, dict]:
        """Fetch latest quote data for one or more tickers.

        Returns:
            dict[str, dict]: With tickers mapped to their quote data
        """
        url = f"{cfg.TIINGO_IEX_URL}{','.join(self.tickers)}"

        response = safe_status_get(url=url, headers=self.HEADERS)
        if not isinstance(response, list):
            logger.error("Tiingo API request Failed")
            return {}
        logger.info("Tiingo API request Successful")

        result = {}
        for entry in response:
            if 'ticker' in entry:
                ticker: str = entry['ticker']
                result[ticker] = dict(entry)
        return result

