"""Balance Sheet metrics."""

import pandas as pd

from qemy.analytics.base import EDGARAnalytics, ResultsDataFrame


class NetDebt(EDGARAnalytics):
    """Net Debt Metric."""

    def __init__(self, ticker: str):
        """Initialize."""
        super().__init__(ticker)

        self.companyanalytics = ResultsDataFrame(
            ticker = self.ticker.upper(),
            entity_name= self.client.companyfacts.entity_name
        )
        self.companyanalytics.description = (
            'Profit a company makes from sales after paying '
            'cost of goods and services (COGS).'
        )

        df_debt: pd.DataFrame = self.get_concept_df_safe('debt')
        df_debt_short: pd.DataFrame = self.get_concept_df_safe('sdebt')
        df_debt_long: pd.DataFrame = self.get_concept_df_safe('ldebt')
        df_cash: pd.DataFrame = self.get_concept_df_safe('cash')
        dfs = [df_cash, df_debt, df_debt_short, df_debt_long]
        self.df_merged = self.merge_concept_dfs(*dfs)

    def calculate(self) -> ResultsDataFrame:
        """Calculate Net Debt metric."""
        df_results = self.df_merged.copy()

        df_results['val'] = (
            df_results['val_debt']
            + df_results['val_sdebt']
            + df_results['val_ldebt']
            - df_results['val_cash']
        )

        df_results.drop(
            ['val_debt', 'val_sdebt', 'val_ldebt', 'val_cash'],
            axis = 1,
            inplace = True
        )
        df_results.sort_values('filed', inplace=True)
        df_results['val'] = df_results['val'].astype(float).fillna(0)
        self.companyanalytics.results_df = df_results

        return self.companyanalytics

