"""Financial Ratio Metrics."""

from typing import cast

import pandas as pd

from qemy.analytics.base import EDGARAnalytics, ResultsDataFrame
from qemy.utils.dataframes import divide_safe, rolling_mean


class RatioAssetTurnover(EDGARAnalytics):
    """Asset Turnover Ratio Calculator."""

    def __init__(self, ticker: str):
        """Initialize calculation components and results container."""
        super().__init__(ticker)

        self.companyanalytics = ResultsDataFrame(
            ticker = self.ticker.upper(),
            name = self.client.companyfacts.name
        )
        self.companyanalytics.description = (
            'Asset Turnover Ratio measures of how efficiently a company '
            'uses its assets to generate revenue.'
        )

        df_assets: pd.DataFrame = self.get_concept_df('assets')
        df_revenue: pd.DataFrame = self.get_concept_df('revenue')
        self.df_merged = self.merge_concept_dfs(*[df_assets, df_revenue])

    def calculate(self) -> ResultsDataFrame:
        """Calculate Asset Turnover Ratio."""
        df_results = self.df_merged.copy()

        series_assets = cast(pd.Series, df_results['val_assets'])
        df_results['avg_assets'] = rolling_mean(series_assets, 4)
        df_results['val'] = divide_safe(
            numerator = cast(pd.Series, df_results['val_revenue']),
            denominator = cast(pd.Series, df_results['avg_assets'])
        )

        df_results.drop(
            ['avg_assets', 'val_assets', 'val_revenue'],
            axis = 1,
            inplace = True
        )
        df_results.sort_values('filed', inplace=True)
        df_results['val'] = df_results['val'].astype(float).fillna(0)
        self.companyanalytics.results_df = df_results

        return self.companyanalytics

class RatioCurrent(EDGARAnalytics):
    """Current Ratio calculator."""

    def __init__(self, ticker: str):
        """Initialize calculation components and results container."""
        super().__init__(ticker)

        self.companyanalytics = ResultsDataFrame(
            ticker = self.ticker.upper(),
            name = self.client.companyfacts.name
        )
        self.companyanalytics.description = (
            "Current Ratio measures a company's liquidity "
            'by comparing current assets to its current liabilities.'
        )

        df_assets: pd.DataFrame = self.get_concept_df('assets')
        df_liab: pd.DataFrame = self.get_concept_df('liab')
        self.df_merged = self.merge_concept_dfs(*[df_assets, df_liab])

    def calculate(self) -> ResultsDataFrame:
        """Calculate Current Ratio."""
        df_results = self.df_merged.copy()

        df_results['val'] = divide_safe(
            numerator = cast(pd.Series, df_results['val_assets']),
            denominator = cast(pd.Series, df_results['val_liab'])
        )

        df_results.drop(
            ['val_assets', 'val_liab'],
            axis = 1,
            inplace = True
        )
        df_results.sort_values('filed', inplace=True)
        df_results['val'] = df_results['val'].astype(float).fillna(0)
        self.companyanalytics.results_df = df_results

        return self.companyanalytics

class RatioROA(EDGARAnalytics):
    """Return on Assets Ratio calculator."""

    def __init__(self, ticker: str):
        """Initialize calculation components and results container."""
        super().__init__(ticker)

        self.companyanalytics = ResultsDataFrame(
            ticker = self.ticker.upper(),
            name = self.client.companyfacts.name
        )
        self.companyanalytics.description = (
            "Return on Assets Ratio measures a company's profitability "
            'by comparing its current net income to its current assets.'
        )

        df_netinc: pd.DataFrame = self.get_concept_df('netinc')
        df_assets: pd.DataFrame = self.get_concept_df('assets')
        self.df_merged = self.merge_concept_dfs(*[df_netinc, df_assets])

    def calculate(self) -> ResultsDataFrame:
        """Calculate Return on Assets Ratio."""
        df_results = self.df_merged.copy()

        df_results['val'] = divide_safe(
            numerator = cast(pd.Series, df_results['val_netinc']),
            denominator = cast(pd.Series, df_results['val_assets'])
        )

        df_results.drop(
            ['val_netinc', 'val_assets'],
            axis = 1,
            inplace = True
        )
        df_results.sort_values('filed', inplace=True)
        df_results['val'] = df_results['val'].astype(float).fillna(0)
        self.companyanalytics.results_df = df_results

        return self.companyanalytics

