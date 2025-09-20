"""Cash-Flow Statment metrics."""

import pandas as pd

from qemy.analytics.base import EDGARAnalytics


class FreeCashFlow(EDGARAnalytics):
    """Calculate Free Cash Flow."""

    def __init__(self, ticker: str):
        """Initialize combined concept DataFrame."""
        super().__init__(ticker)
        df_ocf: pd.DataFrame = self.get_concept_df('ocf')
        df_capex: pd.DataFrame = self.get_concept_df('capex')
        self.df_combined = self.merge_concept_dfs(*[df_ocf, df_capex])

    def get_fcf(self) -> pd.DataFrame:
        """Get Free Cash Flow DataFrame."""
        self.df_combined['val'] = (
            self.df_combined['val_ocf'] - self.df_combined['val_capex']
        )
        df_fcf = self.df_combined.drop(['val_ocf', 'val_capex'], axis=1)

        return df_fcf.sort_values('filed')

