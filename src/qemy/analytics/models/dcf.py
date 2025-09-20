"""Discounted Cash-Flow model."""

from typing import cast

import pandas as pd

from qemy.analytics.base import EDGARAnalytics
from qemy.analytics.metrics.balance_sheet import NetDebt
from qemy.analytics.metrics.cashflow_statement import FreeCashFlow
from qemy.exceptions import AnalyticsModelError


class DCFModel(EDGARAnalytics):
    """Discounted Cash Flow model."""

    def __init__(self, ticker: str):
        """Initialize DCF component metrics."""
        super().__init__(ticker)

        try:
            # Free Cash Flow
            df_fcf: pd.DataFrame = FreeCashFlow(self.ticker).get_fcf()
            # Keep FY (fiscal year) filing rows only
            df_fcf_fiscal_year = df_fcf[df_fcf['fp'] == 'FY']
            self.series_fcf = cast(pd.Series, df_fcf_fiscal_year['val'])

            # Current Net Debt
            self.netdebt: float = NetDebt(
                self.ticker
            ).get_netdebt()['val'].iloc[-1]

            # Current Shares Outstanding
            self.shares: float = self.get_concept_df(
                'shares'
            )['val_shares'].iloc[-1]

        except Exception as e:
            raise AnalyticsModelError('[DCF] Initialization Error') from e

    def _fcf_baseline(self) -> float:
        """Calculate Free Cash Flow 5-year rolling average."""
        series_fcf_rolling_avg = self.series_fcf.rolling(window=5).median()

        return cast(pd.Series, series_fcf_rolling_avg).iloc[-1]

    def _fcf_growth(self) -> float:
        """Calculate CAGR from historical Free Cash Flow values."""
        positive_fcf = self.series_fcf[self.series_fcf > 0]
        positive_fcf = cast(pd.Series, positive_fcf)
        if len(positive_fcf) < 2:
            return 0.07

        start, end = positive_fcf.iloc[0], positive_fcf.iloc[-1]
        n = len(positive_fcf) - 1

        return (end /start) ** (1 / n) - 1

    def _project_fcf(self, years: int=5) -> pd.Series:
        """Projected future Free Cash Flow using constant growth."""
        baseline = self._fcf_baseline()
        growth = self._fcf_growth()

        projected = pd.Series(
            [baseline * (1 + growth) ** t for t in range(1, years + 1)]
        )

        return projected

    def _discount_fcf(
        self,
        projected_fcf: pd.Series,
        rate: float = 0.08
    ) -> pd.Series:
        """Discount projected FCF back to present value."""
        discount_factors = [
            (1 + rate) ** t for t in range(1, len(projected_fcf) + 1)
        ]
        discounted = projected_fcf / discount_factors

        return pd.Series(discounted, index=projected_fcf.index)

    def calculate(
        self,
        years: int = 5,
        discount_rate: float = 0.08,
        terminal_growth: float = 0.03
    ) -> float:
        """Calculate DCF valuation per share.

        - Calculate Free Cash Flow (FCF) baseline and growth
        - Projects future FCF using `fcf_growth`
        - Discounts back to present value using `discount_rate`
        - Calculate terminal value using Gordon Growth method
        - Derive Equity Value = Enterprise Value - Net Debt
        - Calculate per share value = Equity Value / Shares Outstanding

        Args:
            years (int): Number of years to project
            discount_rate (float): Discounting rate
            terminal_growth (float): Long term growth rate

        Returns:
            float: Estimated DCF valuation per share
        """
        # Project FCF
        projected = self._project_fcf(years=years)

        # Discount Projected FCF
        discounted = self._discount_fcf(
            projected_fcf = projected,
            rate = discount_rate
        )

        # Add terminal value
        fcf_final = projected.iloc[-1]
        tv = (
            fcf_final
            * (1 + terminal_growth)
            / (discount_rate - terminal_growth)
        )
        tv_pv = tv / (1 + discount_rate)**years

        # Enterprise Value
        ev = discounted.sum() + tv_pv

        # Equity and per share value
        equity_value = ev - self.netdebt
        per_share_value = equity_value / self.shares

        return per_share_value if per_share_value > 0.0 else 0.0

