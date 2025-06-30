from qemy.data.api_tiingo import TiingoClient
from qemy.data.api_fred import FREDData

def ratio_sharpe(ticker, period='1Y'):
    price_df = TiingoClient().get_prices(ticker=ticker, period=period)
    if price_df.empty:
        return {}

    rfr_df = FREDData().get_tbill_yield()
    if rfr_df is not None and not rfr_df.empty:
        rfr = rfr_df['value'].iloc[0] / 100
    else:
        print(f"No Observations found for T-Bill yield")
        return {}

    pct_df = price_df['adjClose'].pct_change().dropna()
    year_mean = pct_df.mean() * 252
    year_std = pct_df.std() * (252 ** 0.5)

    sharpe_ratio = (year_mean - rfr) / year_std

    return {
        'ticker': ticker,
        'rfr': rfr,
        'mean': year_mean,
        'std': year_std,
        'sharpe': sharpe_ratio
    }

def max_dd(ticker, period='1Y'):
    price_df = TiingoClient().get_prices(ticker=ticker, period=period)
    if price_df.empty:
        return {}

    running_max = price_df['adjClose'].cummax()
    drawdowns = (price_df['adjClose'] - running_max) / running_max
    max_drawdown = drawdowns.min()

    return {
        'ticker': ticker,
        'maxdd': max_drawdown
    }

def volatility(ticker, period='1Y'):
    price_df = TiingoClient().get_prices(ticker=ticker, period=period)
    if price_df.empty:
        return {}

    pct_df = price_df['adjClose'].pct_change().dropna()
    annual_std = pct_df.std() * (252 ** 0.5)

    return {
        'ticker': ticker,
        'vol': annual_std
    }

def beta(ticker):
    return

def sortino(ticker):
    return

def calmar(ticker):
    return

