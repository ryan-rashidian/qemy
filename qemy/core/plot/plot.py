import matplotlib.pyplot as plt
import pandas as pd
from qemy.utils.filetools import save_to_png
from qemy.data.api_tiingo import StockMarket

def plot_models(title='title', save=False, plot_func=None):
    plt.figure(figsize=(14, 8))
    if plot_func:
        plot_func()

    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.tight_layout()

    if save == True:
        save_to_png(filename="modelchart")
    plt.show()

def plot_price(ticker, period):
    stock_data = StockMarket().get_prices(ticker=ticker, period=period)
    stock_df = pd.DataFrame(stock_data)
    stock_df['date'] = pd.to_datetime(stock_df['date'])

    plt.figure(figsize=(14, 8))
    plt.plot(stock_df['date'], stock_df['close'], label='Price', color='green', linewidth=3, marker= 'o', alpha=0.8)
    if len(stock_df['date']) >= 250:
        stock_df['50_DMA'] = stock_df['close'].rolling(window=50).mean()
        stock_df['200_DMA'] = stock_df['close'].rolling(window=200).mean()
        plt.plot(stock_df['date'], stock_df['50_DMA'], label='50 DMA', color='blue', linewidth=1, alpha=0.5)
        plt.plot(stock_df['date'], stock_df['200_DMA'], label='200 DMA', color='red', linewidth=2, alpha=0.5)
    plt.xlabel('Date')
    plt.ylabel('Price (Log-Scale)')
    plt.yscale('log')
    plt.title('Log-Scaled Daily Closing Prices')
    plt.grid(True, which='both')
    plt.legend()
    plt.tight_layout()
    plt.show()

