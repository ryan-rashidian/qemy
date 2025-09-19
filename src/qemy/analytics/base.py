"""Base classes for Qemy Analytics."""

from functools import reduce

import pandas as pd

from qemy.clients import EDGARClient


class AnalysisBase:
    """Base class for Qemy Analytics."""

    def __init__(self):
        """Initialize base."""

class EDGARMetrics:
    """Base class for EDGAR Metrics."""

    def __init__(self, ticker: str):
        """Initialize Client for EDGAR Metrics."""
        self.ticker = ticker.strip()
        self.client = EDGARClient(self.ticker)

    def get_concept_df(self, concept: str) -> pd.DataFrame:
        """Return pandas DataFrame of given concept."""
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

    def merge_concept_dfs(self, *dataframes: pd.DataFrame) -> pd.DataFrame:
        """Merge concept dataframes."""
        df_merged = reduce(
            lambda df_left, df_right: pd.merge(
                df_left,
                df_right,
                on=['filed', 'form'],
                how='outer'
            ),
            dataframes
        )

        df_merged.fillna(0, inplace=True)

        return df_merged

class ModelsBase(AnalysisBase):
    """Base class for Models."""

class RatiosBase(AnalysisBase):
    """Base class for Ratios."""

class ScoresBase(AnalysisBase):
    """Base class for Scores."""

