import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from qemy.data.api_edgar import SEC_Filings
from qemy.core.plugin_base import BasePlugin

class DCFPlugin(BasePlugin):
    name = "dcf"
    description = "Discounted Cash Flow Valuation Model"
    version = "0.1.0"

    def run(self):
        filing_df, shares_outstanding, net_debt = SEC_Filings(ticker=self.ticker).get_dcf_metrics()

        if isinstance(filing_df, pd.DataFrame) and shares_outstanding is not None:
            try:
                fcf_df = filing_df['fcf'].rolling(window=4).mean().dropna().values

                if len(fcf_df) < 4:
                    self.log("Not enough FCF data to apply rolling average.")
                    return

                x_time = np.arange(len(fcf_df)).reshape(-1, 1)
                y_fcf = fcf_df
                model = LinearRegression().fit(X=x_time, y=y_fcf)

                future_x = np.arange(len(fcf_df), len(fcf_df) + 20).reshape(-1, 1)
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
                    intrinsic_value_per_share = max(0, equity_value / shares_outstanding)
                    return {
                        "text": {
                            "Model Fit Confidence": f"{r_squared:.2%}",
                            "Enterprise Value": f"{enterprise_value:.0f}",
                            "Equity Value": f"{equity_value:.0f}",
                            "Intrinsic Value Per Share": f"{intrinsic_value_per_share:.2f}",
                        }
                    }
                else:
                    enterprise_value_per_share = max(0, enterprise_value / shares_outstanding)
                    return {
                        "text": {
                            "Model Fit Confidence": r_squared,
                            "Enterprise Value": enterprise_value,
                            "Enterprise Value Per Share": enterprise_value_per_share,
                        }
                    }

            except Exception as e:
                self.log(f"core/models/dcf.py Exception ERROR:\n{e}")
                return None
        else:
            self.log(f"core/models/dcf.py ERROR:\n{filing_df}\nShares outstanding: {shares_outstanding}")
            return None

    def help(self):
        return (
            f"{self.name.upper()} Plugin Help:\n"
            f"Description: {self.description}\n"
            f"Version: {self.version}\n\n"
            f"Usage: qemy> m dcf -t <TICKER>\n"
        )
    
