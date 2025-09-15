"""Concept parsing and mapping.

Assemble Concept dataclass containers from raw companyfacts data.
"""

from qemy.clients.edgar.schemas import Concept
from qemy.exceptions import ClientParsingError


class ConceptParser:
    """Concept parser for EDGAR client."""

    def __init__(self, raw_facts: dict):
        """Initialize raw companyfacts data."""
        self.raw_facts = raw_facts

    def _map_concept(self, xbrl_mappings: tuple[str]) -> dict:
        """Map XBRL tags to standardized concept data.

        Args:
            xbrl_mappings (tuple[str]): Concept mapping container

        Returns:
            dict: Of filing data for specific concept

        Raises:
            ClientParsingError: If no matches are found
        """
        for map in xbrl_mappings:
            if map not in self.raw_facts['facts']['us-gaap']:
                continue

            return self.raw_facts['facts']['us-gaap'][map]

        raise ClientParsingError('Mapping: No matches found.')

    def _get_units(self, units_dict: dict | None) -> str:
        """Get unit key value for concept.

        Args:
            units_dict (dict | None): Concept 'units' dict

        Returns:
            str: Of unit key value

        Raises:
            ClientParsingError: If there is no data
        """
        if not units_dict:
            raise ClientParsingError('Filing data not found.')

        return next(iter(units_dict))

    def parse(self, xbrl_mapping: tuple[str]) -> Concept:
        """Get parsed Concept from an xbrl_mapping.

        Args:
            xbrl_mappings (tuple[str]): Concept mapping container

        Returns:
            Concept: Parsed concept data
        """
        concept: dict = self._map_concept(xbrl_mapping)
        label: str = concept.get('label', '')
        description: str = concept.get('description', '')
        unit: str = self._get_units(concept.get('units'))

        concept_files: list = concept['units'][unit]
        concept_files_parsed = [
            f for f in concept_files if 'frame' in f.keys()
        ]

        return Concept(
            label = label,
            description = description,
            unit = unit,
            filings = concept_files_parsed
        )

