"""Dataclasses representing intermediate structures of SEC filing data.

These classes provide containers for companyfacts and concepts.
Used by EDGARClient and ConceptParser within the EDGAR client.
"""

import pandas as pd

from dataclasses import dataclass, field


@dataclass
class Concept:
    """Container for parsed filings and metadata."""
    label: str
    description: str
    unit: str
    filings: list[dict]

    def __repr__(self) -> str:
        return (
            f"Concept(label='{self.label}', unit='{self.unit}', "
            f"filings=#{len(self.filings)} filed)"
        )

    def to_dataframe(self) -> pd.DataFrame:
        """Format Concept filings into pandas DataFrame.

        Returns:
            pd.DataFrame: of Concept filings
        """
        concept_df = pd.DataFrame(self.filings)
        concept_df['filed'] = pd.to_datetime(
            concept_df['filed'],
            errors='coerce'
        )
        concept_df.dropna(subset=['filed'], inplace=True)
        concept_df.sort_values('filed', inplace=True)
        concept_df.drop_duplicates('frame', keep='last', inplace=True)
        concept_df.reset_index(drop=True, inplace=True)
        concept_df['val'] = concept_df['val'].astype(float)
        return concept_df

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

