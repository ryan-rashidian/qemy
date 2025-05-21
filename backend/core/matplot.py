import matplotlib.pyplot as plt
import pandas as pd
from backend.fetch.api_tiingo import get_tiingo_prices

def plot_price(ticker, period):
    data = get_tiingo_prices(ticker=ticker, period=period)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    plt.figure(figsize=(14, 7))
    plt.plot(df['date'], df['close'], label='Price', color='green', linewidth=3, marker= 'o', alpha=0.8)
    if len(df['date']) >= 250:
        df['50_DMA'] = df['close'].rolling(window=50).mean()
        df['200_DMA'] = df['close'].rolling(window=200).mean()
        plt.plot(df['date'], df['50_DMA'], label='50 DMA', color='blue', linewidth=1, alpha=0.5)
        plt.plot(df['date'], df['200_DMA'], label='200 DMA', color='red', linewidth=2, alpha=0.5)
    plt.xlabel('Date')
    plt.ylabel('Price (Log-Scale)')
    plt.yscale('log')
    plt.title('Log-Scaled Daily Closing Prices')
    plt.grid(True, which='both')
    plt.legend()
    plt.tight_layout()
    plt.show()
