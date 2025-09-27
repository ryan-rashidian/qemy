"""Tiingo Client for Qemy.

This module handles requests and fetching data from Tiingo API.
"""

from __future__ import annotations

from typing import Self

import pandas as pd

from qemy.clients.tiingo.schemas import (
    PriceData,
    QuoteData,
    decode_prices_json,
    decode_quotes_json,
)
from qemy.config.credentials import require_credential
from qemy.config.urls import TIINGO_IEX_URL, TIINGO_URL
from qemy.exceptions import InvalidArgumentError
from qemy.utils.dates import parse_period
from qemy.utils.networking import make_request


class TiingoClient:
    """Client for fetching stock market data from Tiingo API."""

    RESAMPLE_ALLOWED = {'daily', 'weekly', 'monthly', 'annually'}
    PRICE_COLUMNS = ['adjClose', 'adjHigh', 'adjLow', 'adjOpen', 'adjVolume']

    def __init__(self, ticker: str | list[str]):
        """Initialize Client with credentials and request headers.

        Normalize ticker argument to list[str]
        Construct instance of HEADERS with user credentials

        Args:
            ticker (str | list[str]): Company ticker symbol(s)
        """

        self.tickers = []
        if isinstance(ticker, str):
            self.tickers = [ticker.strip().upper()]
        elif isinstance(ticker, list):
            self.tickers = [t.strip().upper() for t in ticker]

        self.price_data = {}
        self.quote_data = []

        self.HEADERS: dict[str, str] = {'Content-Type': 'application/json'}

    def __repr__(self) -> str:
        return f"TiingoClient(ticker={self.tickers})"

    def __str__(self) -> str:
        return f"[TiingoClient]\nticker={self.tickers}"

    def __bool__(self) -> bool:
        return bool(self.tickers)

    def __len__(self) -> int:
        return len(self.tickers)

    def __getitem__(self, position: int) -> str:
        return self.tickers[position]

    def __add__(self, other: list) -> TiingoClient:
        """Add a list of tickers to self and return new Client."""
        new_tickers = self.tickers.copy()
        for ticker in other:
            if ticker.strip().upper() not in new_tickers:
                new_tickers.append(ticker.strip().upper())
        return TiingoClient(new_tickers)

    def __sub__(self, other: list) -> TiingoClient:
        """Subtract a list of tickers from self and return new Client."""
        remove = set(ticker.strip().upper() for ticker in other)
        new_tickers = [t for t in self.tickers if t not in remove]
        return TiingoClient(new_tickers)

    def __iadd__(self, other: list) -> Self:
        """Add a list of tickers to Client in-place."""
        for ticker in other:
            if ticker.strip().upper() not in self.tickers:
                self.tickers.append(ticker.strip.upper())
        return self

    def __isub__(self, other: list) -> Self:
        """Subtract a list of tickers from Client in-place."""
        remove = set(ticker.strip().upper() for ticker in other)
        self.tickers = [t for t in self.tickers if t not in remove]
        return self

    def _check_param(self, check_set: set, param: str) -> str:
        """Verify if param argument is allowed."""
        if param not in check_set:
            raise InvalidArgumentError(
                'Incorrect argument for param.\n'
                f'Given: {param}\n'
                f'Accepted: {check_set}'
            )
        return param

    def _get_price_params(
        self,
        period: str,
        resample: str,
    ) -> dict:
        """Get a formatted parameter dictionary for Tiingo requests."""
        credential: str = require_credential(
            service = 'Tiingo',
            env_var = 'TIINGO_API_KEY'
        )
        start, end = parse_period(period_str=period)
        resample_checked = self._check_param(
            param = resample,
            check_set = self.RESAMPLE_ALLOWED
        )

        return {
            'startDate': start,
            'endDate': end,
            'resampleFreq': resample_checked,
            'columns': ','.join(self.PRICE_COLUMNS),
            'token': credential
        }

    def fetch_prices(
        self,
        period: str,
        resample: str = 'daily',
    ) -> Self:
        """Fetch historical price data for initialized ticker(s).

        Args:
            period (str): Date window starting from current
                - e.g '2D', '3M', '2Y', '2W'
            resample (str): Frequency of data sampling
                - e.g. 'daily', 'weekly', 'monthly'
            columns (list[str]): Data fields for request
                - e.g. 'close', 'volume', 'open'

        Raises:
            InvalidArgumentError: If a parameter string is not valid
        """
        for ticker in self.tickers:
            url = f'{TIINGO_URL}{ticker}/prices'
            params: dict = self._get_price_params(
                period = period,
                resample = resample,
            )

            price_json: str = make_request(
                url = url,
                headers = self.HEADERS,
                params = params
            )
            price_data: list[PriceData] = decode_prices_json(price_json)
            self.price_data[ticker] = price_data

        return self

    def to_dataframe_prices(self) -> dict[str, pd.DataFrame]:
        """Format Tiingo price data into pandas DataFrame.

        Returns:
            dict[str, pd.DataFrame]: Of price data mapped to tickers
        """
        price_dataframes = {}

        for ticker, price_data in self.price_data.items():
            price_df = pd.DataFrame([dict(entry) for entry in price_data])

            if 'date' in price_df.columns:
                price_df['date'] = pd.to_datetime(price_df['date'])
                price_df.set_index('date', inplace=True)
                price_df.sort_index(inplace=True)

            price_dataframes[ticker] = price_df

        return price_dataframes

    def fetch_quote(self) -> Self:
        """Fetch latest price quote for initialized ticker(s)."""
        url = f"{TIINGO_IEX_URL}{','.join(self.tickers)}"
        credential: str = require_credential(
            service = 'Tiingo',
            env_var = 'TIINGO_API_KEY'
        )
        params = {'token': credential}

        quote_json: str = make_request(
            url = url,
            headers = self.HEADERS,
            params = params
        )
        self.quote_data: list[QuoteData] = decode_quotes_json(quote_json)

        return self

    def to_dataframe_quote(self) -> pd.DataFrame:
        """Format Tiingo quote data into pandas DataFrame.

        Returns:
            pd.DataFrame: Of quote data
        """
        return pd.DataFrame([dict(entry) for entry in self.quote_data])

