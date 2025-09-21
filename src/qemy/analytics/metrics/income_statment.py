"""Income Statement metrics."""

import pandas as pd

from qemy.analytics.base import EDGARAnalytics, ResultsDataFrame


class GrossMargin(EDGARAnalytics):
    """Gross Margin calculator."""

    def __init__(self, ticker: str):
        """Initialize calculation components and result container."""
        super().__init__(ticker)

        self.companyanalytics = ResultsDataFrame(
            ticker = self.ticker.upper(),
            entity_name= self.client.companyfacts.entity_name
        )
        self.companyanalytics.description = (
            'Profit a company makes from sales after paying '
            'cost of goods and services (COGS).'
        )

        df_gprofit: pd.DataFrame = self.get_concept_df('gprofit')
        df_revenue: pd.DataFrame = self.get_concept_df('revenue')
        self.df_combined = self.merge_concept_dfs(*[df_gprofit, df_revenue])

    def calculate(self) -> ResultsDataFrame:
        """Calculate Gross Margin value.

        Returns:
            CompanyAnalytics: Container with results + metadata
        """
        self.df_combined['val'] = (
            self.df_combined['val_gprofit'] / self.df_combined['val_revenue']
        )
        self.df_combined.drop(
            ['val_gprofit', 'val_revenue'],
            axis = 1,
            inplace = True
        )
        self.df_combined.sort_values('filed', inplace=True)
        self.companyanalytics.results_df = self.df_combined

        return self.companyanalytics

