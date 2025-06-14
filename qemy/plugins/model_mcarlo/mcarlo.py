import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qemy.data.api_tiingo import get_tiingo_prices

def monte_carlo_sim(ticker, period='1Y', num=1000, **_):
    try:
        num_days = None
        data = get_tiingo_prices(ticker=ticker, period=period)
        data = pd.DataFrame(data)

        if isinstance(data, pd.DataFrame):
            close_prices = np.array(data['close'])
            past_returns = (close_prices[1:] / close_prices[:-1]) - 1
            past_mean = np.mean(past_returns)
            past_std = np.std(past_returns)

            if num_days is None:
                num_days = len(data['close'])
            start_price = close_prices[-1]
            simulations = np.zeros((num, num_days))

            for i in range(num):
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
                    "# of Simulations": num,
                    "End Mean": f"{end_mean:.2f}",
                    "End STD": f"{end_std:.2f}",
                },
                "plot": {
                    "title": f"{num }Monte Carlo Simulation for {ticker}",
                    "plot_func": lambda: (
                        plt.plot(simulations.T, alpha=0.05, color='blue'),
                    )
                },
            }

        else:
            print(f"Failed to retrieve price data for {ticker}")
            return None

    except Exception as e:
        print(f"core/models/monte_carlo.py Exception ERROR:\n{e}")
        return None

