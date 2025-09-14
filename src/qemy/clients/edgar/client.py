"""EDGAR client orchestrator for SEC EDGAR data pipeline.

Handles the process of:
- Fetching data
- Parsing data
- Mapping concepts
- Normalizing data shape
"""

from qemy.clients.edgar import _mappings
from qemy.clients.edgar.fetcher import FactsLoader
from qemy.clients.edgar.parser import ConceptParser
from qemy.clients.edgar.schemas import CompanyFacts, Concept
from qemy.exceptions import InvalidArgumentError

class EDGARClient:
    """EDGAR client orchestrator class."""

    def __init__(self, ticker: str):
        """Initialize data pipeline for client."""
        self.raw_facts: dict = FactsLoader(ticker).get_companyfacts()
        self.parser = ConceptParser(self.raw_facts)
        self.companyfacts = CompanyFacts(
            ticker = ticker.strip().upper(),
            entity_name = self.raw_facts.get('entityName', '')
        )

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

    def get_concept(self, concept: str) -> None:
        """Fetches parsed filing data for given concept.

        Args:
            concept (str): Key for matching concept tuple
            quarters (int): Number of fiscal quarters to fetch
        """
        xbrl_mappings = self._get_mappings(concept)
        parsed_data: Concept = self.parser.parse(xbrl_mappings)
        self.companyfacts.concepts[concept] = parsed_data

    def fill_concepts(self) -> None:
        """"""
        
