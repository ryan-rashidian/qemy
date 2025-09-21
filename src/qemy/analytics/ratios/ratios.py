"""Financial Ratio Metrics."""

import pandas as pd

from qemy.analytics.base import EDGARAnalytics, ResultsDataFrame

class RatioCurrent(EDGARAnalytics):
    """Current Ratio calculator."""

    def __init__(self, ticker: str):
        """Initialize calculation components and results container."""
        super().__init__(ticker)

        self.companyanalytics = ResultsDataFrame(
            ticker = self.ticker.upper(),
            entity_name = self.client.companyfacts.entity_name
        )
        self.companyanalytics.description = (
            "Current Ratio measures a company's liquidity "
            'by comparing current assets to its current liabilities.'
        )

        df_assets: pd.DataFrame = self.get_concept_df('assets')
        df_liab: pd.DataFrame = self.get_concept_df('liab')
        self.df_combined = self.merge_concept_dfs(*[df_assets, df_liab])

    def calculate(self) -> ResultsDataFrame:
        """Calculate Current Ratio."""
        self.df_combined['val'] = (
            self.df_combined['val_assets'] / self.df_combined['val_liab']
        )
        self.df_combined.drop(
            ['val_assets', 'val_liab'],
            axis = 1,
            inplace = True
        )
        self.df_combined.sort_values('filed', inplace=True)
        self.companyanalytics.results_df = self.df_combined

        return self.companyanalytics

class RatioROA(EDGARAnalytics):
    """Return on Assets Ratio calculator."""

    def __init__(self, ticker: str):
        """Initialize calculation components and results container."""
        super().__init__(ticker)

        self.companyanalytics = ResultsDataFrame(
            ticker = self.ticker.upper(),
            entity_name = self.client.companyfacts.entity_name
        )
        self.companyanalytics.description = (
            "Return on Assets Ratio measures a company's profitability "
            'by comparing its current net income to its current assets.'
        )

        df_netinc: pd.DataFrame = self.get_concept_df('netinc')
        df_assets: pd.DataFrame = self.get_concept_df('assets')
        self.df_combined = self.merge_concept_dfs(*[df_netinc, df_assets])

    def calculate(self) -> ResultsDataFrame:
        """Calculate Return on Assets Ratio."""
        self.df_combined['val'] = (
            self.df_combined['val_netinc'] / self.df_combined['val_assets']
        )
        self.df_combined.drop(
            ['val_netinc', 'val_assets'],
            axis = 1,
            inplace = True
        )
        self.df_combined.sort_values('filed', inplace=True)
        self.companyanalytics.results_df = self.df_combined

        return self.companyanalytics

