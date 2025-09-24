"""Dataclasses representing intermediate structures of SEC filing data.

These classes provide containers for companyfacts and concepts.
Used by EDGARClient and ConceptParser within the EDGAR client.
"""

from dataclasses import dataclass, field

import pandas as pd

from qemy.utils.dataframes import normalize_financial_df


@dataclass
class Concept:
    """Container for parsed filings and metadata."""
    label: str = ''
    description: str = ''
    unit: str = ''
    filings: list[dict] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Concept(label='{self.label}', unit='{self.unit}')"

    def __len__(self) -> int:
        return len(self.filings)

    def to_dataframe(self) -> pd.DataFrame:
        """Format Concept filings into pandas DataFrame.

        Returns:
            pd.DataFrame: of Concept filings
        """
        concept_df = pd.DataFrame(self.filings)
        return normalize_financial_df(
            df = concept_df,
            value_col = 'val',
            date_col = 'filed'
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
            f"entity_name='{self.entity_name}')"
        )

    def __len__(self) -> int:
        return len(self.concepts)

