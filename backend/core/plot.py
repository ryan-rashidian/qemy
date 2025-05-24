import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
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

def plot_lr(ticker, period):
    input_data = get_tiingo_prices(ticker=ticker, period=period)
    auto_data = get_tiingo_prices(ticker='SPY', period=period)
    input_df, auto_df = pd.DataFrame(input_data), pd.DataFrame(auto_data)
    input_df.set_index('date', inplace=True)
    input_df.index = pd.to_datetime(input_df.index)
    auto_df.set_index('date', inplace=True)
    auto_df.index = pd.to_datetime(auto_df.index)
    data = pd.DataFrame({
        ticker: input_df['close'], 
        'SPY': auto_df['close']
    }).dropna()
    returns = data.pct_change().dropna()
    x_ind = np.array(returns['SPY']).reshape(-1, 1) 
    y_dep = np.array(returns[ticker])

    model = LinearRegression()
    model.fit(x_ind, y_dep)
    alpha = model.intercept_
    beta = model.coef_[0]

    print(f"Alpha: {alpha:.6f}")
    print(f"Beta: {beta:.4f}")

    plt.figure(figsize=(8, 5))
    plt.scatter(x_ind, y_dep, alpha=0.4, label='Returns')
    plt.plot(x_ind, model.predict(x_ind), color='red', label='Regression Line')
    plt.xlabel('SPY Daily Returns')
    plt.ylabel(f"{ticker} Daily Returns")
    plt.title(f"{ticker} vs SPY Beta Regression")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
