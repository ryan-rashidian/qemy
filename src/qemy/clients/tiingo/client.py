"""Tiingo Client for Qemy.

This module handles requests and fetching data from Tiingo API.
"""

from __future__ import annotations

from qemy.utils.dates import parse_period
from qemy.config.credentials import require_credential
from qemy.utils.networking import make_request
from qemy.exceptions import InvalidArgumentError
from qemy.config.urls import TIINGO_IEX_URL, TIINGO_URL

class TiingoClient:
    """Client for fetching stock market data from Tiingo API."""

    # Possible arguments for resample and column parameters
    RESAMPLE_ALLOWED = {'daily', 'weekly', 'monthly', 'annually'}
    COLUMNS_ALLOWED = {
        'close', 'high', 'low', 'open', 'volume',
        'adjClose', 'adjHigh', 'adjLow', 'adjOpen', 'adjVolume',
        'divCash', 'splitFactor'
    }

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

    def _check_param(self, check_set: set, param: str) -> str:
        """Verify if param argument is allowed."""
        if param not in check_set:
            raise InvalidArgumentError(
                'Incorrect argument for param.\n'
                f'Given: {param}\n'
                f'Accepted: {check_set}'
            )
        return param

    def _get_params(
        self,
        period: str,
        resample: str,
        columns: list[str]
    ) -> dict:
        """Get a formatted parameter dictionary for Tiingo requests."""
        start, end = parse_period(period_str=period)
        resample_checked = self._check_param(
            param = resample,
            check_set = self.RESAMPLE_ALLOWED
        )
        columns_checked = []
        for col in columns:
            columns_checked.append(self._check_param(
                param = col,
                check_set = self.COLUMNS_ALLOWED
            ))

        return {
            'startDate': start,
            'endDate': end,
            'resampleFreq': resample_checked,
            'columns': columns_checked
        }

    def get_prices(self):
        """"""




