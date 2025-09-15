"""Tiingo Client for Qemy.

This module handles requests and fetching data from Tiingo API.
"""

from __future__ import annotations

from qemy.config.credentials import require_credential
from qemy.utils.networking import make_request
from qemy.exceptions import InvalidArgumentError

# Argument verification sets for Client
resample_check = {'daily', 'weekly', 'monthly', 'annually'}
columns_check = {
    'close', 'high', 'low', 'open', 'volume',
    'adjClose', 'adjHigh', 'adjLow', 'adjOpen', 'adjVolume',
    'divCash', 'splitFactor'
}

class TiingoClient:
    """Client for fetching stock market data from Tiingo API."""

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
        
        credential: str = require_credential(
            service = 'Tiingo',
            env_var = 'TIINGO_API_KEY'
        )
        self.HEADERS: dict[str, str] = {
            'Content-Type': 'application/json',
            'Authorization': credential
        }

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

    def __iadd__(self, other: list) -> TiingoClient:
        """Add a list of tickers to Client in-place."""
        for ticker in other:
            if ticker.strip().upper() not in self.tickers:
                self.tickers.append(ticker.strip.upper())
        return self

    def __isub__(self, other: list) -> TiingoClient:
        """Subtract a list of tickers from Client in-place."""
        remove = set(ticker.strip().upper() for ticker in other)
        self.tickers = [t for t in self.tickers if t not in remove]
        return self





