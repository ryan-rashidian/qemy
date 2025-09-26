"""Companyfacts data fetching.

Load a given companies file from SEC EDGAR companyfacts.
"""

from pathlib import Path

from qemy.clients.edgar.schemas import (
    CompanyCIK,
    CompanyFacts,
    decode_cik_json,
    decode_companyfacts_json,
)
from qemy.config.credentials import require_credential
from qemy.config.paths import COMPANY_TICKERS_JSON, COMPANYFACTS_UNZIPPED
from qemy.config.urls import EDGAR_CIK_URL, EDGAR_FACTS_URL
from qemy.exceptions import ClientDataError
from qemy.utils.networking import make_request


class FactsLoader:
    """Companyfacts data fetcher for EDGAR client"""

    def __init__(self, ticker: str):
        """Initialize company ticker."""
        self.ticker = ticker.lower().strip()

    @property
    def needs_request(self) -> bool:
        """Return True if local bulk data is not found."""
        required_paths = [COMPANY_TICKERS_JSON, COMPANYFACTS_UNZIPPED]
        return not all(path.exists() for path in required_paths)

    def _request_companyfacts(self) -> CompanyFacts:
        """Request companyfacts JSON file from SEC EDGAR API."""
        cred = require_credential(service='EDGAR', env_var='EDGAR_USER_AGENT')
        headers = {'User-Agent': cred}

        cik_json: str = make_request(url=EDGAR_CIK_URL, headers=headers)
        cik_data: CompanyCIK = decode_cik_json(cik_json, ticker=self.ticker)
        cik = str(cik_data.cik).zfill(10)
        cik_facts_url = f'{EDGAR_FACTS_URL}CIK{cik}.json'

        companyfacts_json: str = make_request(
            url=cik_facts_url,
            headers=headers
        )
        return decode_companyfacts_json(companyfacts_json)

    def _load_json(self, path: Path) -> str:
        """Load JSON file with error handling."""
        try:
            with open(path, 'r') as f:
                return f.read()

        except Exception as e:
            raise ClientDataError(f'Error reading: {path.resolve()}') from e

    def _load_companyfacts(self) -> CompanyFacts:
        """Load companyfacts JSON file locally."""
        cik_json = self._load_json(COMPANY_TICKERS_JSON)
        cik_data: CompanyCIK = decode_cik_json(cik_json, ticker=self.ticker)
        cik = str(cik_data.cik).zfill(10)
        companyfacts_file = COMPANYFACTS_UNZIPPED / f'CIK{cik}.json'

        companyfacts_json: str = self._load_json(companyfacts_file)
        return decode_companyfacts_json(companyfacts_json)

    def get_companyfacts(self) -> CompanyFacts:
        """Returns companyfacts JSON file for initialized ticker."""
        if self.needs_request:
            return self._request_companyfacts()

        return self._load_companyfacts()

