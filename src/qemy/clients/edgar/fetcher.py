"""Companyfacts data fetching.

Load a given companies file from SEC EDGAR companyfacts.
"""

import json
from pathlib import Path

from qemy.config.credentials import require_credential
from qemy.config.paths import COMPANY_TICKERS_JSON, COMPANYFACTS_UNZIPPED
from qemy.config.urls import EDGAR_CIK_URL, EDGAR_FACTS_URL
from qemy.exceptions import ClientDataError
from qemy.utils.networking import make_request


class FactsLoader:
    """Companyfacts data fetcher for EDGAR client"""

    def __init__(self, ticker: str):
        """Initialize attributes."""
        self.ticker = ticker.lower().strip()
        self.cik_data = {}
        self.cik = None

    @property
    def needs_request(self) -> bool:
        """Return True if local bulk data is not found."""
        required_paths = [COMPANY_TICKERS_JSON, COMPANYFACTS_UNZIPPED]
        return not all(path.exists() for path in required_paths)

    def _load_json(self, path: Path) -> dict:
        """Load JSON file with error handling."""
        try:
            with open(path, 'r') as f:
                return json.load(f)

        except json.JSONDecodeError as e:
            raise ClientDataError(f'Corrupted: {path.resolve()}') from e

        except Exception as e:
            raise ClientDataError(f'Error reading: {path.resolve()}') from e

    def _map_cik(self) -> str:
        """Map company ticker to matching CIK number."""
        for entry in self.cik_data.values():
            if entry.get('ticker', '').lower() == self.ticker:
                cik = entry.get('cik_str')
                if cik is None:
                    raise ClientDataError(
                        f'Missing CIK: {self.ticker.upper()}'
                    )

                return str(cik).zfill(10)

        raise ClientDataError(f'CIK Mapping Error: {self.ticker.upper()}')

    def _request_companyfacts(self) -> dict:
        """Request companyfacts JSON file from SEC EDGAR API."""
        cred = require_credential(service='EDGAR', env_var='EDGAR_USER_AGENT')
        headers = {'User-Agent': cred}

        self.cik_data = make_request(url=EDGAR_CIK_URL, headers=headers)
        self.cik = self._map_cik()
        ticker_facts_url = f'{EDGAR_FACTS_URL}CIK{self.cik}.json'

        return make_request(url=ticker_facts_url, headers=headers)

    def _load_companyfacts(self) -> dict:
        """Load companyfacts JSON file locally."""
        self.cik_data = self._load_json(COMPANY_TICKERS_JSON)
        self.cik = self._map_cik()

        companyfacts_file = COMPANYFACTS_UNZIPPED / f'CIK{self.cik}.json'
        return self._load_json(companyfacts_file)

    def get_companyfacts(self) -> dict:
        """Returns companyfacts JSON file for initialized ticker."""
        if self.needs_request:
            return self._request_companyfacts()

        return self._load_companyfacts()

