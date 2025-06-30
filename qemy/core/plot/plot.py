import matplotlib.pyplot as plt
from qemy.utils.file_tools import save_to_png
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
    stock_df = StockMarket().get_prices(ticker=ticker, period=period)

    plt.figure(figsize=(14, 8))
    plt.plot(stock_df.index, stock_df['adjClose'], label='Price', color='green', linewidth=3, marker= 'o', alpha=0.8)
    if len(stock_df.index) >= 250:
        stock_df['50_DMA'] = stock_df['adjClose'].rolling(window=50).mean()
        stock_df['200_DMA'] = stock_df['adjClose'].rolling(window=200).mean()
        plt.plot(stock_df.index, stock_df['50_DMA'], label='50 DMA', color='blue', linewidth=1, alpha=0.5)
        plt.plot(stock_df.index, stock_df['200_DMA'], label='200 DMA', color='red', linewidth=2, alpha=0.5)
    plt.xlabel('Date')
    plt.ylabel('Price (Log-Scale)')
    plt.yscale('log')
    plt.title('Log-Scaled Daily Closing Prices')
    plt.grid(True, which='both')
    plt.legend()
    plt.tight_layout()
    plt.show()

