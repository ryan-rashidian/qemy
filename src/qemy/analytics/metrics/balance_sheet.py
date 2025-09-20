"""Balance Sheet metrics."""

import pandas as pd

from qemy.analytics.base import EDGARMetrics


class NetDebt(EDGARMetrics):
    """Net Debt Metric."""

    def __init__(self, ticker: str):
        """Initialize."""
        super().__init__(ticker)

        df_debt = self.get_concept_df_safe('debt')
        df_debt_short = self.get_concept_df_safe('sdebt')
        df_debt_long = self.get_concept_df_safe('ldebt')
        df_cash = self.get_concept_df_safe('cash')
        dfs = [df_cash, df_debt, df_debt_short, df_debt_long]
        self.df_combined = self.merge_concept_dfs(*dfs)

    def get_netdebt(self) -> pd.DataFrame:
        """Calculate Net Debt metric."""
        self.df_combined['val'] = (
            self.df_combined['val_debt']
            + self.df_combined['val_sdebt']
            + self.df_combined['val_ldebt']
            - self.df_combined['val_cash']
        )
        df_netdebt = self.df_combined.drop(
            ['val_debt', 'val_sdebt', 'val_ldebt', 'val_cash'],
            axis = 1
        )

        return df_netdebt

