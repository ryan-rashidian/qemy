"""
Containers representing intermediate structures for SEC filing data.

Using dataclasses for companyfacts and parsed concepts.
"""

from dataclasses import dataclass, field


@dataclass
class Concept:
    """Container for parsed filings and metadata."""
    tag: str
    label: str
    description: str
    unit: str
    filings: list[dict]

    def __repr__(self) -> str:
        return (
            f"Concept(tag='{self.tag}', label='{self.label}', "
            f"unit='{self.unit}', filings=#{len(self.filings)} filed)"
        )

@dataclass
class CompanyFacts:
    """Container for parsed and sorted companyfacts data."""
    ticker: str
    entity_name: str
    concepts: dict[str, Concept] = field(default_factory=dict)

    def __repr__(self) -> str:
        return (
            f"CompanyFacts(ticker='{self.ticker}', "
            f"entity_name='{self.entity_name}', "
            f'concepts=#{len(self.concepts)} concepts)'
        )

