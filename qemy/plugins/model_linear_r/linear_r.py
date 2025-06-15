import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from qemy.data.api_tiingo import StockMarket
from qemy.core.plugin_base import BasePlugin

class LinearRPlugin(BasePlugin):
    name = "linear_r"
    description = "Linear Regression Model"
    version = "0.1.0"

    def run(self):
        try:
            ind_data = StockMarket().get_prices(ticker=self.ticker, period=self.period)
            dep_data = StockMarket().get_prices(ticker='SPY', period=self.period)

            ind_df, dep_df = pd.DataFrame(ind_data), pd.DataFrame(dep_data)
            ind_df.set_index('date', inplace=True)
            ind_df.index = pd.to_datetime(ind_df.index)
            dep_df.set_index('date', inplace=True)
            dep_df.index = pd.to_datetime(dep_df.index)
            data = pd.DataFrame({
                self.ticker: ind_df['close'], 
                'SPY': dep_df['close']
            }).dropna()
            returns = data.pct_change().dropna()

            x_axis = np.array(returns['SPY']).reshape(-1, 1) 
            y_axis = np.array(returns[self.ticker])

            model = LinearRegression()
            model.fit(X=x_axis, y=y_axis)
            alpha = model.intercept_
            beta = model.coef_[0]

            return {
                "text": {
                    "Alpha": f"{alpha:.4f}",
                    "Beta": f"{beta:.4f}",
                },
                "plot": {
                    "title": f"Linear Regression fit for {self.ticker} and SPY returns",
                    "plot_func": lambda: (
                        plt.scatter(x_axis, y_axis, alpha=0.3),
                        plt.plot(x_axis, model.predict(x_axis), color='red')
                    )
                },
            }

        except Exception as e:
            print(f"core/models/linear_r.py Exception ERROR:\n{e}")
            return None 

