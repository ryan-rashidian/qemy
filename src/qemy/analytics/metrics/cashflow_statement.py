"""Cash-Flow Statment metrics."""

import pandas as pd

from qemy.analytics.base import EDGARAnalytics, ResultsDataFrame


class FreeCashFlow(EDGARAnalytics):
    """Calculate Free Cash Flow."""

    def __init__(self, ticker: str):
        """Initialize combined concept DataFrame."""
        super().__init__(ticker)

        self.companyanalytics = ResultsDataFrame(
            ticker = self.ticker.upper(),
            name= self.client.companyfacts.name
        )
        self.companyanalytics.description = (
            'Profit a company makes from sales after paying '
            'cost of goods and services (COGS).'
        )

        df_ocf: pd.DataFrame = self.get_concept_df('ocf')
        df_capex: pd.DataFrame = self.get_concept_df('capex')
        self.df_merged = self.merge_concept_dfs(*[df_ocf, df_capex])

    def calculate(self) -> ResultsDataFrame:
        """Get Free Cash Flow DataFrame."""
        df_results = self.df_merged.copy()

        df_results['val'] = df_results['val_ocf'] - df_results['val_capex']

        df_results.drop(['val_ocf', 'val_capex'], axis=1, inplace=True)
        df_results.sort_values('filed', inplace=True)
        df_results['val'] = df_results['val'].astype(float).fillna(0)
        self.companyanalytics.results_df = df_results

        return self.companyanalytics

