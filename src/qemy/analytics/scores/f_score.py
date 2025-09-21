"""Piotroski F-Score Calculator."""

import pandas as pd

from qemy.analytics.base import CompanyAnalytics, ResultsScalar, EDGARAnalytics
from qemy.analytics.ratios.ratios import (
    RatioAssetTurnover,
    RatioCurrent,
    RatioROA
)
from qemy.analytics.metrics.income_statment import GrossMargin

class PiotroskiFScore(EDGARAnalytics):
    """Piotroski F-Score Calculator."""

    def __init__(self, ticker: str):
        """Initialize calculation component and results container."""
        super().__init__(ticker)

        self.companyanalytics = ResultsScalar(
            ticker = self.ticker.upper(),
            entity_name = self.client.companyfacts.entity_name
        )
        self.companyanalytics.description = (
            "Piotroski F-Score is a 0-9 score that measures a company's "
            'financial strength based on several fundamental factors.'
        )

        self.netinc, self.ocf = 0, 0

    def _fscore_netinc(self) -> int:
        """Net Income"""
        try:
            df_netinc: pd.DataFrame = self.get_concept_df('netinc')
            self.netinc = df_netinc['val'].iloc[-1]

        except Exception:
            return 0

        return 1 if self.netinc > 0 else 0

    def _fscore_ocf(self) -> int:
        """Operating Cash Flow"""
        try:
            df_ocf: pd.DataFrame = self.get_concept_df('ocf')
            self.ocf = df_ocf['val'].iloc[-1]

        except Exception:
            return 0

        return 1 if self.ocf > 0 else 0

    def _fscore_accruals(self) -> int:
        """Accruals"""
        return 1 if self.ocf > self.netinc else 0

    def _fscore_roa(self) -> int:
        """Return on Assets"""
        try:
            roa_results: CompanyAnalytics = RatioROA(self.ticker).calculate()
            current_roa = roa_results.results_df['val'].iloc[-1]
            previous_roa = roa_results.results_df['val'].iloc[-5]

        except Exception:
            return 0

        return 1 if current_roa > previous_roa else 0

    def _fscore_ldebt(self) -> int:
        """Long Term Debt"""
        try:
            df_ldebt: pd.DataFrame = self.get_concept_df('ldebt')
            current_ldebt = df_ldebt['val'].iloc[-1]
            previous_ldebt = df_ldebt['val'].iloc[-1]

        except Exception:
            return 1

        return 1 if previous_ldebt > current_ldebt else 0

    def _fscore_cratio(self) -> int:
        """Current Ratio"""
        try:
            cratio_results: CompanyAnalytics = RatioCurrent(
                self.ticker
            ).calculate()
            current_cratio = cratio_results.results_df['val'].iloc[-1]
            previous_cratio = cratio_results.results_df['val'].iloc[-5]

        except Exception:
            return 0

        return 1 if current_cratio > previous_cratio else 0

    def _fscore_shares(self) -> int:
        """Shares Outstanding"""
        try:
            df_shares: pd.DataFrame = self.get_concept_df('shares')
            current_shares = df_shares['val'].iloc[-1]
            previous_shares = df_shares['val'].iloc[-1]

        except Exception:
            return 0

        return 1 if previous_shares >= current_shares else 0

    def _fscore_gmargin(self) -> int:
        """Gross Margin"""
        try:
            gmargin_results: CompanyAnalytics = GrossMargin(
                self.ticker
            ).calculate()
            current_gmargin = gmargin_results.results_df['val'].iloc[-1]
            previous_gmargin = gmargin_results.results_df['val'].iloc[-5]

        except Exception:
            return 0

        return 1 if current_gmargin > previous_gmargin else 0

    def _fscore_asset_turnover(self) -> int:
        """Asset Turnover"""
        try:
            at_results: CompanyAnalytics = RatioAssetTurnover(
                self.ticker
            ).calculate()

            current_at = at_results.results_df['val'].iloc[-1]
            previous_at = at_results.results_df['val'].iloc[-5]

        except Exception:
            return 0

        return 1 if current_at > previous_at else 0

    def calculate(self) -> ResultsScalar:
        """Calculate Piotroski F-Score."""
        fscore_netinc = self._fscore_netinc()
        fscore_ocf = self._fscore_ocf()
        fscore_accruals = self._fscore_accruals()
        fscore_roa = self._fscore_roa()
        fscore_ldebt = self._fscore_ldebt()
        fscore_cratio = self._fscore_cratio()
        fscore_shares = self._fscore_shares()
        fscore_gmargin = self._fscore_gmargin()
        fscore_asset_turnover = self._fscore_asset_turnover()

        f_score = (
            fscore_netinc
            + fscore_ocf
            + fscore_accruals
            + fscore_roa
            + fscore_ldebt
            + fscore_cratio
            + fscore_shares
            + fscore_gmargin
            + fscore_asset_turnover
        )
        self.companyanalytics.results['f_score'] = f_score

        return self.companyanalytics

