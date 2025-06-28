import pandas as pd
from qemy.data.api_tiingo import StockMarket
from qemy.data.api_edgar import SEC_Filings

def cagr(ticker, period='1Y'):
    price_data = StockMarket().get_prices(ticker=ticker, period=period)

    try:
        price_df = pd.DataFrame(price_data)
    except:
        print(f"No price data found for: {ticker}")
        return {}

    price_df['date'] = pd.to_datetime(price_df['date'])
    price_df.set_index('date', inplace=True)
    n_years = (price_df.index[-1] - price_df.index[0]).days / 365

    start_price = price_df['adjClose'].iloc[0]
    end_price = price_df['adjClose'].iloc[-1]

    cagr = (end_price / start_price) ** (1 / n_years) - 1  

    return {
        'ticker': ticker,
        'years': n_years,
        'cagr': cagr
    }

def growth_rate(ticker, metric):
    metric_data = SEC_Filings(ticker=ticker).get_metric_history(key=metric.lower())
    metric_vals = metric_data['val'].iloc[-5:]
    metric_growth = metric_vals.pct_change().dropna()

    annual_metric_growth = (1 + metric_growth).prod() - 1
    
    return {
        'ticker': ticker,
        'growth': annual_metric_growth
    }

def eps_growth(ticker):
    return

