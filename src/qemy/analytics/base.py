"""Base classes for Qemy Analytics."""

from dataclasses import dataclass, field
from functools import reduce

import pandas as pd

from qemy.clients import EDGARClient
from qemy.exceptions import ClientParsingError


@dataclass
class CompanyAnalytics:
    """Container for company analytics results."""
    ticker: str
    entity_name: str = ''
    description: str = ''

@dataclass
class ResultsScalar(CompanyAnalytics):
    """Company analytics with scalar results."""
    results: dict[str, float] = field(default_factory=dict)

@dataclass
class ResultsDataFrame(CompanyAnalytics):
    """Company analytics with DataFrame results."""
    results_df: pd.DataFrame = field(default_factory=pd.DataFrame)

class EDGARAnalytics:
    """Base class for EDGAR Metrics."""

    def __init__(self, ticker: str):
        """Initialize Client for EDGAR Metrics."""
        self.ticker = ticker.strip()
        self.client = EDGARClient(self.ticker)

    def get_concept_df(self, concept: str) -> pd.DataFrame:
        """Return pandas DataFrame of a concept."""
        concept_fmt = concept.strip().lower()
        df_concept = self.client.get_concept(
            concept = concept_fmt
        ).companyfacts.concepts[concept].to_dataframe()

        if 'val' in df_concept.columns:
            df_concept.rename(
                columns = {'val': f'val_{concept_fmt}'},
                inplace = True
            )

        return df_concept

    def get_concept_df_safe(self, concept: str) -> pd.DataFrame:
        """Return pandas DataFrame of a concept.

        Return placeholder DataFrame if parsing error occurs.
        """
        concept_fmt = concept.strip().lower()

        try:
            df_concept = self.client.get_concept(
                concept = concept_fmt
            ).companyfacts.concepts[concept].to_dataframe()
        except ClientParsingError:
            column_template = ['fp', 'fy', 'filed', 'form', 'frame', 'val']
            columns = pd.Index(column_template)
            df_concept = pd.DataFrame(columns=columns)
            df_concept['val'] = df_concept['val'].astype(float)

        if 'val' in df_concept.columns:
            df_concept.rename(
                columns = {'val': f'val_{concept_fmt}'},
                inplace = True
            )

        return df_concept

    def merge_concept_dfs(self, *dataframes: pd.DataFrame) -> pd.DataFrame:
        """Merge concept dataframes."""

        def merge(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
            """Merge on common columns"""
            common = [c for c in left.columns if c in right.columns]
            return pd.merge(left, right, on=common, how='outer')

        df_merged = reduce(merge, dataframes)
        df_merged.fillna(0, inplace=True)

        if 'accn' in df_merged.columns:
            df_merged.drop_duplicates('accn', keep='last', inplace=True)

        return df_merged

