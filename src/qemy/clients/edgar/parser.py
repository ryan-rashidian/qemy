"""
Concept parsing and mapping.

Assemble Concept dataclass containers from raw companyfacts data.
"""

from qemy.exceptions import ClientParsingError
from qemy.clients.edgar.schemas import CompanyFacts, Concept

class ConceptParser:
    """Concept parser for EDGAR client."""

    def __init__(self, companyfacts: CompanyFacts):
        self.companyfacts = companyfacts

