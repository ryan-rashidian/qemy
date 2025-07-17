"""FRED API module.

This module requests and fetches data from FRED API.
"""

import logging

import pandas as pd

from qemy import _config as cfg
from qemy.exceptions import DataError

from ._api_tools import parse_period, safe_status_get

logger = logging.getLogger(__name__)

class FREDClient:
    """Client for fetching macro-economic data from FRED API."""

    def __init__(self):
        """Initialize FREDClient with API key and URL."""
        self.API_KEY: str = cfg.fred_api_key()
        self.url: str = cfg.FRED_URL

    def __repr__(self) -> str:
        return "FREDClient()"

    def __str__(self) -> str:
        return "[FREDClient]"

    def _fetch_series(
        self,
        series_id: str,
        period: str='1Y',
        frequency: str='m',
        units: str='pc1',
        aggregation: str='avg',
        limit: int=100_000
    ) -> pd.DataFrame:
        """Internal method for sending requests.

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
            limit (int): Integer to slice tail of observations

        Returns:
            pd.DataFrame: DataFrame indexed by 'date' with 'val' column

        Raises:
            APIClientError: If failure to fetch observations
        """
        start_date, end_date = parse_period(period)

        params = {
            'series_id': series_id,
            'api_key': self.API_KEY,
            'file_type': 'json',
            'sort_order': 'desc',
            'observation_start': start_date,
            'observation_end': end_date,
            'frequency': frequency,
            'units': units,
            'aggregation_method': aggregation,
            'limit': limit
        }

        fred_data = safe_status_get(url=self.url, params=params)
        try:
            obs_df = pd.DataFrame(fred_data['observations'])
            obs_df['date'] = pd.to_datetime(obs_df['date'])
            obs_df.set_index('date', inplace=True)
            obs_df['value'] = pd.to_numeric(
                obs_df['value'],
                errors='coerce'
            )
            # Rename column to 'val' for consistency
            obs_df.rename(columns={'value': 'val'}, inplace=True)
            # Drop un-needed columns
            return obs_df.drop(
                columns=['realtime_start', 'realtime_end'],
                errors='ignore'
            )

        except Exception as e:
            logger.error(e)
            raise DataError("[FREDClient] No observations found") from e

    def get_tbill_yield(self) -> pd.DataFrame:
        """Fetch latest observation for: 1 Year T-Bill Yield."""
        return self._fetch_series(
            series_id='GS1',
            period='1M',
            frequency='m',
            units='lin',
            limit=1
        )

    def get_cpi(
        self,
        period: str='1Y',
        units: str='pc1'
    ) -> pd.DataFrame:
        """Fetch observations for: Consumer Price Index.

        Args:
            period (str): Period for requested data
                - (e.g., "1Y", "3M")
            units (str): Units of measurement for observations
                - (e.g., "pc1", "pch", "lin")
        """
        return self._fetch_series(
            series_id='CPIAUCSL',
            period=period,
            frequency='m',
            units=units
        )

    def get_gdp(
        self,
        period: str='1Y',
        units: str='pc1'
    ) -> pd.DataFrame:
        """Fetch observations for: Gross Domestic Product.

        Args:
            period (str): Period for requested data
                - (e.g., "1Y", "3M")
            units (str): Units of measurement for observations
                - (e.g., "pc1", "pch", "lin")
        """
        return self._fetch_series(
            series_id='GDP',
            period=period,
            frequency='q',
            units=units
        )

    def get_sentiment(
        self,
        period: str='1Y',
        units: str='pch'
    ) -> pd.DataFrame:
        """Fetch observations for: Consumer Sentiment Index.

        Args:
            period (str): Period for requested data
                - (e.g., "1Y", "3M")
            units (str): Units of measurement for observations
                - (e.g., "pc1", "pch", "lin")
        """
        return self._fetch_series(
            series_id='UMCSENT',
            period=period,
            frequency='m',
            units=units
        )

    def get_nf_payrolls(
        self,
        period: str='1Y',
        units: str='pc1'
    ) -> pd.DataFrame:
        """Fetch observations for: Nonfarm Payrolls.

        Args:
            period (str): Period for requested data
                - (e.g., "1Y", "3M")
            units (str): Units of measurement for observations
                - (e.g., "pc1", "pch", "lin")
        """
        return self._fetch_series(
            series_id='PAYEMS',
            period=period,
            frequency='m',
            units=units
        )

    def get_interest_rate(
        self,
        period: str='1Y',
        units: str='pc1'
    ) -> pd.DataFrame:
        """Fetch observations for: Federal Interest Rate.

        Args:
            period (str): Period for requested data
                - (e.g., "1Y", "3M")
            units (str): Units of measurement for observations
                - (e.g., "pc1", "pch", "lin")
        """
        return self._fetch_series(
            series_id='DFF',
            period=period,
            frequency='d',
            units=units
        )

    def get_jobless_claims(
        self,
        period: str='1Y',
        units: str='pc1'
    ) -> pd.DataFrame:
        """Fetch observations for: Jobless Claims.

        Args:
            period (str): Period for requested data
                - (e.g., "1Y", "3M")
            units (str): Units of measurement for observations
                - (e.g., "pc1", "pch", "lin")
        """
        return self._fetch_series(
            series_id='ICSA',
            period=period,
            frequency='w',
            units=units
        )

    def get_unemployment(
        self,
        period: str='1Y',
        units: str='pc1'
    ) -> pd.DataFrame:
        """Fetch observations for: Unemployment Rate.

        Args:
            period (str): Period for requested data
                - (e.g., "1Y", "3M")
            units (str): Units of measurement for observations
                - (e.g., "pc1", "pch", "lin")
        """
        return self._fetch_series(
            series_id='UNRATE',
            period=period,
            frequency='m',
            units=units
        )

    def get_industrial_production(
        self,
        period: str='1Y',
        units: str='pc1'
    ) -> pd.DataFrame:
        """Fetch observations for: Industrial Production Index.

        Args:
            period (str): Period for requested data
                - (e.g., "1Y", "3M")
            units (str): Units of measurement for observations
                - (e.g., "pc1", "pch", "lin")
        """
        return self._fetch_series(
            series_id='INDPRO',
            period=period,
            frequency='m',
            units=units
        )

    def get_net_exports(
        self,
        period: str='1Y',
        units: str='lin'
    ) -> pd.DataFrame:
        """Fetch observations for: Net Exports.

        Args:
            period (str): Period for requested data
                - (e.g., "1Y", "3M")
            units (str): Units of measurement for observations
                - (e.g., "pc1", "pch", "lin")
        """
        return self._fetch_series(
            series_id='NETEXC',
            period=period,
            frequency='q',
            units=units
        )

