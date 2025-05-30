from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utils.filetools import get_next_path
from sklearn.linear_model import LinearRegression
from backend.fetch.api_tiingo import get_tiingo_prices
from backend.fetch import api_fred as fred

project_root = Path(__file__).resolve().parents[2]
export_dir = project_root / "exports" / "charts"
export_dir.mkdir(parents=True, exist_ok=True)

def plot_price(ticker, period):
    data = get_tiingo_prices(ticker=ticker, period=period)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])

    plt.figure(figsize=(14, 8))
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
    model.fit(X=x_ind, y=y_dep)
    alpha = model.intercept_
    beta = model.coef_[0]
    print(f"Alpha: {alpha:.6f}")
    print(f"Beta: {beta:.4f}")

    plt.figure(figsize=(14, 8))
    plt.scatter(x_ind, y_dep, alpha=0.4, label='Returns')
    plt.plot(x_ind, model.predict(x_ind), color='red', label='Regression Line')
    plt.xlabel('SPY Daily Returns')
    plt.ylabel(f"{ticker} Daily Returns")
    plt.title(f"{ticker} vs SPY Beta Regression")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_cpi(period, save=False):
    data = fred.get_cpi_inflation(period=period)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='CPI Inflation', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Inflation')
    plt.title('CPI Inflation: % Change from Year Ago')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='cpichart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()
    
def plot_gdp(period, save=False):
    data = fred.get_gdp(period=period)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='GDP', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('GDP')
    plt.title('GDP: % Change from Year Ago')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='gdpchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_sentiment(period, save=False):
    data = fred.get_sentiment(period=period)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='Sentiment', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Sentiment')
    plt.title('Sentiment: % Change')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='sentchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_nfp(period, save=False):
    data = fred.get_nf_payrolls(period=period)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='NFP', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('NFP')
    plt.title('Non-Farm Payrolls: % Change from Year Ago')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='nfpchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_interest(period, save=False):
    data = fred.get_interest(period=period)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='interest', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Interest')
    plt.title('Interest: % Change from Year Ago')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='interestchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_jobc(period, save=False):
    data = fred.get_jobless_claims(period=period)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='jobless claims', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Jobless Claims')
    plt.title('Jobless Claims: % Change from Year Ago')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='jobcchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_unemployment(period, save=False):
    data = fred.get_unemployment(period=period)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='unemployment', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Unemployment rate')
    plt.title('Unemployment rate: % Change from Year Ago')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='unemchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_ind_prod(period, save=False):
    data = fred.get_ind_prod(period=period)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='ind prod', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Ind Prod')
    plt.title('Industrial Production: % Change from Year Ago')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='indpchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_composite(period, save=False):
    data = fred.get_composite(period=period)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='composite index', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Composite index')
    plt.title('Composite index: % Change from Year Ago')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='compchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

