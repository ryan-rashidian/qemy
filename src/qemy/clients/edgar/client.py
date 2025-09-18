"""EDGAR client orchestrator for SEC EDGAR data pipeline.

Handles the process of:
- Fetching data
- Parsing data
- Mapping concepts
- Normalizing data shape
"""

from __future__ import annotations

from qemy.clients.edgar import _mappings
from qemy.clients.edgar.fetcher import FactsLoader
from qemy.clients.edgar.parser import ConceptParser
from qemy.clients.edgar.schemas import CompanyFacts, Concept
from qemy.exceptions import InvalidArgumentError


class EDGARClient:
    """EDGAR client orchestrator class."""

    def __init__(self, ticker: str):
        """Initialize EDGAR data pipeline for given company.

        Args:
            ticker (str): Company ticker symbol
        """
        self.raw_facts: dict = FactsLoader(ticker).get_companyfacts()
        self.parser = ConceptParser(self.raw_facts)
        self.companyfacts = CompanyFacts(
            ticker = ticker.strip().upper(),
            entity_name = self.raw_facts.get('entityName', '')
        )

    def __repr__(self) -> str:
        return f'EDGARClient({self.companyfacts.ticker})'

    def __str__(self) -> str:
        return f'[EDGAR Client]: {self.companyfacts.ticker}'

    def __bool__(self) -> bool:
        return bool(self.raw_facts)

    def __len__(self) -> int:
        return len(self.companyfacts.concepts)

    def _get_mappings(self, concept: str) -> tuple[str]:
        """Get matching tuple for concept mapping.

        Args:
            concept (str): Key for matching concept tuple

        Returns:
            tuple[str]: Matching concept mapper

        Raises:
            InvalidArgumentError: If undefined concept key is given
        """
        try:
            section, label = _mappings.map_arg[concept.lower()]
            return _mappings.filing_tags[section][label]

        except KeyError as e:
            raise InvalidArgumentError(f'{concept} is undefined') from e

    def get_concept(self, concept: str) -> EDGARClient:
        """Fetches parsed filing data for given concept.

        Args:
            concept (str): Key for matching concept tuple
        """
        xbrl_mappings = self._get_mappings(concept)
        parsed_data: Concept = self.parser.parse(xbrl_mappings)
        self.companyfacts.concepts[concept] = parsed_data
        return self

    def fill_concepts(self) -> EDGARClient:
        """Fetch and parse all filing data."""
        for concept in _mappings.map_arg.keys():
            xbrl_mappings = self._get_mappings(concept)
            parsed_data: Concept = self.parser.parse(xbrl_mappings)
            self.companyfacts.concepts[concept] = parsed_data
        return self

