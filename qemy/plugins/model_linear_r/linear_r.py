import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from qemy.data import TiingoClient
from qemy.plugins import BasePlugin

class LinearRPlugin(BasePlugin):
    name = "linear_r"
    description = "Linear Regression Model"
    version = "0.1.1"

    def run(self):
        try:
            ticker_df = TiingoClient().get_prices(ticker=self.ticker, period=self.period)
            spy_df = TiingoClient().get_prices(ticker='SPY', period=self.period)

            combined_df = pd.DataFrame({
                self.ticker: ticker_df['adjClose'], 
                'SPY': spy_df['adjClose']
            }).dropna()

            returns_df = combined_df.pct_change().dropna()

            x_spy = np.array(returns_df['SPY']).reshape(-1, 1) 
            y_ticker = np.array(returns_df[self.ticker])

            model = LinearRegression()
            model.fit(X=x_spy, y=y_ticker)

            alpha = model.intercept_
            alpha_annual = alpha * 252
            beta = model.coef_[0]

            return {
                "text": {
                    "Alpha": f"{alpha:.2%} daily | {alpha_annual:.2%} annualized",
                    "Beta": f"{beta:.4f}",
                },
                "plot": {
                    "title": f"Linear Regression fit for {self.ticker} and SPY returns",
                    "plot_func": lambda: (
                        plt.scatter(x_spy, y_ticker, alpha=0.3),
                        plt.plot(x_spy, model.predict(x_spy), color='red')
                    )
                },
            }

        except Exception as e:
            self.log(f"core/models/linear_r.py Exception ERROR:\n{e}")
            return None 

    def help(self):
        return (
            f"{self.name.upper()} Plugin Help:\n"
            f"Description: {self.description}\n"
            f"Version: {self.version}\n\n"
            f"Usage: qemy> m linear_r -t <TICKER> -p <PERIOD>\n"
        )
    
