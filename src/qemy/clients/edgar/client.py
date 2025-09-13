"""
EDGAR client orchestrator for SEC EDGAR data pipeline.

Handles the process of:
- Fetching data
- Parsing data
- Mapping concepts
- Normalizing data shape
"""

from qemy.clients.edgar.fetcher import FactsLoader
from qemy.clients.edgar.schemas import CompanyFacts

class EDGARClient:
    """EDGAR client orchestrator class."""

    def __init__(self, ticker: str):
        """Initialize data pipeline for client."""
        self.raw_facts: dict = FactsLoader(ticker).get_companyfacts()
        self.companyfacts = CompanyFacts(
            ticker = ticker.strip().upper(),
            entity_name = self.raw_facts.get('entityName', '')
        )
        
