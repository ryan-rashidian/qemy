"""Income Statement metrics."""

from typing import cast

import pandas as pd

from qemy.utils.dataframes import divide_safe
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
        self.df_merged = self.merge_concept_dfs(*[df_gprofit, df_revenue])

    def calculate(self) -> ResultsDataFrame:
        """Calculate Gross Margin value.

        Returns:
            CompanyAnalytics: Container with results + metadata
        """
        df_results = self.df_merged.copy()

        df_results['val'] = divide_safe(
            numerator = cast(pd.Series, df_results['val_gprofit']),
            denominator = cast(pd.Series, df_results['val_revenue'])
        ).fillna(0)

        df_results.drop(
            ['val_gprofit', 'val_revenue'],
            axis = 1,
            inplace = True
        )
        df_results.sort_values('filed', inplace=True)
        self.companyanalytics.results_df = df_results

        return self.companyanalytics

