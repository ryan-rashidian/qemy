from math import nan

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from qemy.data import EDGARClient
from qemy.plugins import BasePlugin


class DCFPlugin(BasePlugin):
    name = "dcf"
    description = "Discounted Cash Flow Valuation Model"
    version = "0.1.1"

    def _get_dcf_metrics(self):

        try:
            df_shares = EDGARClient(self.ticker).get_concept(
                concept='shares',
                quarters=10
            )
            if df_shares is None:
                shares = nan
            else:
                shares = df_shares['val'].iloc[-1]

            df_debt = EDGARClient(self.ticker).get_concept(
                concept='debt',
                quarters=10
            )
            df_debt_short = EDGARClient(self.ticker).get_concept(
                concept='sdebt',
                quarters=10
            )
            df_debt_long = EDGARClient(self.ticker).get_concept(
                concept='ldebt',
                quarters=10
            )
            df_cash = EDGARClient(self.ticker).get_concept(
                concept='cash',
                quarters=10
            )

            if df_debt is None:
                debt = 0
            else:
                debt = df_debt['val'].iloc[-1]
            if df_debt_short is None:
                debt_short = 0
            else:
                debt_short = df_debt_short['val'].iloc[-1]
            if df_debt_long is None:
                debt_long = 0
            else:
                debt_long = df_debt_long['val'].iloc[-1]
            if df_cash is None:
                cash = 0
            else:
                cash = df_cash['val'].iloc[-1]
            net_debt = (debt + debt_short + debt_long) - cash

            df_ocf = EDGARClient(self.ticker).get_concept(
                concept='ocf',
                quarters=20
            )
            df_capex = EDGARClient(self.ticker).get_concept(
                concept='capex',
                quarters=20
            )
            if df_ocf is None or df_capex is None:
                df_fcf = nan
            else:
                df_cash_combined = pd.merge(
                    df_ocf,
                    df_capex,
                    on='filed',
                    how='outer',
                    suffixes=('_ocf', '_capex')
                ).copy()
                df_combined = df_cash_combined.infer_objects()
                df_combined = df_combined.fillna(0)
                df_combined['val'] = (
                    df_combined['val_ocf'] - df_combined['val_capex']
                )
                df_fcf = df_combined[['filed', 'val']].tail(20).copy()
                df_fcf.set_index('filed', inplace=True)
                if isinstance(df_fcf, pd.DataFrame):
                    df_fcf['val'] = pd.to_numeric(
                        df_fcf['val'],
                        errors='coerce'
                    )

            return df_fcf, shares, net_debt

        except Exception as e:
            print(f"Failed to request EDGARClient:\n{e}")
            return None, None, None

    def run(self) -> dict:
        filing_df, shares, net_debt = self._get_dcf_metrics()

        if isinstance(filing_df, pd.DataFrame) and shares is not None:
            try:
                rolling_window = filing_df['val'].rolling(window=4)
                rolling_mean = pd.Series(rolling_window.mean())
                rolling_mean_clean = rolling_mean.dropna()
                fcf_df = rolling_mean_clean.values

                if len(fcf_df) < 4:
                    self.log("Not enough FCF data to apply rolling average.")
                    return {}

                x_time = np.arange(len(fcf_df)).reshape(-1, 1)
                y_fcf = fcf_df
                model = LinearRegression().fit(X=x_time, y=y_fcf)

                future_x = np.arange(
                    len(fcf_df),
                    len(fcf_df) + 20
                ).reshape(-1, 1)
                fcf_forecast = model.predict(future_x)
                fcf_forecast = np.clip(fcf_forecast, 0, None)

                r_squared = model.score(x_time, y_fcf)

                discount_rate = 0.09 / 4
                quarters = np.arange(1, 21)
                discount_factors = 1 / (1 + discount_rate) ** quarters
                discounted_fcf = fcf_forecast * discount_factors

                g = 0.02
                r = 0.09
                fcf_last = fcf_forecast[-1]
                terminal_value = (fcf_last * (1 + g)) / (r - g)
                n = len(fcf_forecast)
                discounted_tv = terminal_value / ((1 + discount_rate) ** n)

                enterprise_value = np.sum(discounted_fcf) + discounted_tv

                if net_debt:
                    equity_value = enterprise_value - net_debt
                    # Intrinsic Value Per-Share
                    ivps = max(0, equity_value / shares)
                    return {
                        "text": {
                            "Model Fit Confidence": f"{r_squared:.2%}",
                            "Enterprise Value": f"{enterprise_value:.0f}",
                            "Equity Value": f"{equity_value:.0f}",
                            "Intrinsic Value Per Share": f"{ivps:.2f}",
                        }
                    }
                else:
                    # Enterprise Value Per-Share
                    evps = max(0, enterprise_value / shares)
                    return {
                        "text": {
                            "Model Fit Confidence": r_squared,
                            "Enterprise Value": enterprise_value,
                            "Enterprise Value Per Share": evps,
                        }
                    }

            except Exception as e:
                self.log(f"dcf.py Exception ERROR:\n{e}")
                return {}
        else:
            self.log("dcf.py ERROR:")
            self.log(f"{filing_df}")
            self.log(f"Shares outstanding: {shares}")
            return {}

    def help(self):
        return (
            f"{self.name.upper()} Plugin Help:\n"
            f"Description: {self.description}\n"
            f"Version: {self.version}\n\n"
            f"Usage: qemy> m dcf -t <TICKER>\n"
        )

