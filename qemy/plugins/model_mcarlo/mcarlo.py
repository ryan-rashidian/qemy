import numpy as np
import matplotlib.pyplot as plt

from qemy.data import TiingoClient
from qemy.plugins import BasePlugin

class MCarloPlugin(BasePlugin):
    name = "mcarlo"
    description = "Monte Carlo Simulation"
    version = "0.1.0"

    def run(self):
        try:
            num_days = None
            ticker_df = TiingoClient().get_prices(ticker=self.ticker, period=self.period)

            if not ticker_df.empty:
                close_prices = np.array(ticker_df['adjClose'])
                past_returns = (close_prices[1:] / close_prices[:-1]) - 1
                past_mean = np.mean(past_returns)
                past_std = np.std(past_returns)

                if num_days is None:
                    num_days = len(ticker_df['adjClose'])
                start_price = close_prices[-1]
                simulations = np.zeros((self.num, num_days))

                for i in range(self.num):
                    future_returns = np.random.normal(loc=past_mean, scale=past_std, size=num_days)
                    price_path = [start_price]

                    for ret in future_returns:
                        price_path.append(price_path[-1] * (1 + ret))
                    simulations[i] = price_path[1:]

                end_mean = np.mean(simulations[:, -1])
                end_std = np.std(simulations[:, -1])

                return {
                    "text": {
                        "Assumptions": f"Daily % Return mean: {past_mean:.6f}, STD: {past_std:.6f}",
                        "Start Price": f"{start_price:.2f}",
                        "# of Simulations": self.num,
                        "End Mean": f"{end_mean:.2f}",
                        "End STD": f"{end_std:.2f}",
                    },
                    "plot": {
                        "title": f"{self.num} Monte Carlo Simulation for {self.ticker}",
                        "plot_func": lambda: (
                            plt.plot(simulations.T, alpha=0.05, color='blue'),
                        )
                    },
                }

            else:
                self.log(f"Failed to retrieve price data for {self.ticker}")
                return None

        except Exception as e:
            self.log(f"core/models/monte_carlo.py Exception ERROR:\n{e}")
            return None

    def help(self):
        return (
            f"{self.name.upper()} Plugin Help:\n"
            f"Description: {self.description}\n"
            f"Version: {self.version}\n\n"
            f"Usage: qemy> m mcarlo -t <TICKER> -p <PERIOD> -n <#SIMS>\n"
        )
    
