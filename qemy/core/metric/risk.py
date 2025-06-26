import pandas as pd
from qemy.data.api_tiingo import StockMarket
from qemy.data.api_fred import FREDData

def ratio_sharpe(ticker, period='1Y'):
    price_data = StockMarket().get_prices(ticker=ticker, period=period)

    try:
        price_df = pd.DataFrame(price_data)
        pct_df = price_df['close'].pct_change().dropna()
        year_mean = pct_df.mean() * 252
        year_std = pct_df.std() * (252 ** 0.5)
    except:
        return f"No price data found for: {ticker}"

    rfr_df = FREDData().get_tbill_yield()
    if rfr_df is not None and not rfr_df.empty:
        rfr = rfr_df['value'].iloc[0] / 100
    else:
        return f"No Observations found for T-Bill yield"

    sharpe_ratio = (year_mean - rfr) / year_std
    return (
        f"{ticker}\n"
            f"RFR: {rfr:.3f}\n"
            f"1-Year Mean: {year_mean:.3f}\n"
            f"1-Year STD: {year_std:.3f}\n"
            f"Sharpe Ratio: {sharpe_ratio:.2f}"
    )

def max_dd(ticker):
    return

def volatility(ticker):
    return

def beta(ticker):
    return

def sortino(ticker):
    return

def calmar(ticker):
    return

def cagr(ticker):
    return
