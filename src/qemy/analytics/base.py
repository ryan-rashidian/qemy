"""Base classes for Qemy Analytics."""

from functools import reduce

import pandas as pd

from qemy.clients import EDGARClient
from qemy.exceptions import ClientParsingError


class EDGARMetrics:
    """Base class for EDGAR Metrics."""
    ON_COLUMNS = [
        'accn', 'fp', 'fy', 'filed', 'form', 'start', 'end', 'frame'
    ]

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
            columns = pd.Index(self.ON_COLUMNS + ['val'])
            df_concept = pd.DataFrame(columns=columns)

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
                on = self.ON_COLUMNS,
                how = 'outer'
            ),
            dataframes
        )

        df_merged.fillna(0, inplace=True)

        return df_merged

class ModelsBase:
    """Base class for Models."""

class RatiosBase:
    """Base class for Ratios."""

class ScoresBase:
    """Base class for Scores."""

