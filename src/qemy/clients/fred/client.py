"""FRED Client for Qemy.

This module handles requests and fetching data from FRED API.
"""

from __future__ import annotations

from qemy.config.credentials import require_credential
from qemy.config.logger import get_logger
from qemy.config.urls import FRED_URL
from qemy.exceptions import ClientDataError
from qemy.utils.dates import parse_period
from qemy.utils.networking import make_request

logger = get_logger(__name__)

class FREDClient:
    """Client for fetching economic data from FRED API."""

    def __init__(self):
        """Initialize observation dictionary."""
        self.observations = {}

    def __repr__(self) -> str:
        return "FREDClient()"

    def __str__(self) -> str:
        return "[FREDClient]"

    def _fetch_series(
        self,
        seried_id: str,
        period: str = '1y',
        frequency: str = 'm',
        units: str = 'pc1',
        aggregation: str = 'avg',
        limit: int = 100_000
    ) -> None:
        """Internal method for fetching observation data from FRED.

        Args:
            series_id (str): Series ID for observation
            period (str): Period for requested data
                - (e.g., "1Y", "3M")
            frequency (str): Frequency for observations
                - (e.g., "m", "q", "d")
            units (str): Units of measurement for observations
                - (e.g., "pc1", "pch", "lin")
            aggregation (str): Frequency aggregation
                - "avg" Average
                - "sum" Sum
                - "eop" End of Period
            limit (int): Integer for slicing tail of observations

        Raises:
            ClientDataError: If no observation data is found
        """
        start_date, end_date = parse_period(period)
        api_key = require_credential(service='FRED', env_var='FRED_API_KEY')

        params = {
            'series_id': seried_id,
            'api_key': api_key,
            'file_type': 'json',
            'sort_order': 'desc',
            'observation_start': start_date,
            'observation_end': end_date,
            'frequency': frequency,
            'units': units,
            'aggregation_method': aggregation,
            'limit': limit
        }

        fred_data: dict = make_request(url=FRED_URL, params=params)
        if not fred_data:
            logger.error(f'No data found for: {seried_id}')
            raise ClientDataError(f'No data found for: {seried_id}')

        logger.debug(f'[FRED] Add: {seried_id} Period: {period}')
        self.observations[seried_id] = fred_data

    def get_cpi(
        self,
        period: str = '1y',
        units: str = 'pc1'
    ) -> FREDClient:
        """Fetch observations for: Consumer Price Index."""
        self._fetch_series(
            seried_id = 'CPIAUCSL',
            period = period,
            frequency = 'm',
            units = units
        )
        return self

    def get_gdp(
        self,
        period: str = '1y',
        units: str = 'pc1'
    ) -> FREDClient:
        """Fetch observations for: Gross Domestic Product."""
        self._fetch_series(
            seried_id = 'GDP',
            period = period,
            frequency = 'q',
            units = units
        )
        return self

    def get_industrial_production(
        self,
        period: str = '1y',
        units: str = 'pc1'
    ) -> FREDClient:
        """Fetch observations for: Industrial Production Index."""
        self._fetch_series(
            seried_id = 'INDPRO',
            period = period,
            frequency = 'm',
            units = units
        )
        return self

    def get_interest_rate(
        self,
        period: str = '1y',
        units: str = 'pc1'
    ) -> FREDClient:
        """Fetch observations for: Federal Interest Rate."""
        self._fetch_series(
            seried_id = 'DFF',
            period = period,
            frequency = 'd',
            units = units
        )
        return self

    def get_jobless_claims(
        self,
        period: str = '1y',
        units: str = 'pc1'
    ) -> FREDClient:
        """Fetch observations for: Jobless Claims."""
        self._fetch_series(
            seried_id = 'ICSA',
            period = period,
            frequency = 'w',
            units = units
        )
        return self

    def get_net_exports(
        self,
        period: str = '1y',
        units: str = 'lin'
    ) -> FREDClient:
        """Fetch observations for: Net Exports."""
        self._fetch_series(
            seried_id = 'NETEXC',
            period = period,
            frequency = 'q',
            units = units
        )
        return self

    def get_nf_payrolls(
        self,
        period: str = '1y',
        units: str = 'pc1'
    ) -> FREDClient:
        """Fetch observations for: Nonfarm Payrolls."""
        self._fetch_series(
            seried_id = 'PAYEMS',
            period = period,
            frequency = 'm',
            units = units
        )
        return self

    def get_sentiment(
        self,
        period: str = '1y',
        units: str = 'pch'
    ) -> FREDClient:
        """Fetch observations for: Consumer Sentiment Index."""
        self._fetch_series(
            seried_id = 'UMCSENT',
            period = period,
            frequency = 'm',
            units = units
        )
        return self

    def get_tbill_yield(
        self,
        period: str = '1y',
        units: str = 'lin'
    ) -> FREDClient:
        """Fetch observations for: 1-Year T-Bill Yield."""
        self._fetch_series(
            seried_id = 'GS1',
            period = period,
            frequency = 'm',
            units = units
        )
        return self

    def get_unemployment(
        self,
        period: str = '1y',
        units: str = 'pc1'
    ) -> FREDClient:
        """Fetch observations for: Unemployment Rate."""
        self._fetch_series(
            seried_id = 'UNRATE',
            period = period,
            frequency = 'm',
            units = units
        )
        return self

