import pandas as pd

from qemy.data import EDGARClient, SECFiles, TiingoClient


def cagr(ticker, period='1Y'):
    price_df = TiingoClient(ticker=ticker).get_prices(period=period)
    if price_df.empty:
        return {}

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
    metric_concept: SECFiles = EDGARClient(ticker=ticker).get_concept(
        concept=metric
    )
    metric_df: pd.DataFrame = metric_concept.data

    metric_vals = metric_df['val'].iloc[-5:]
    metric_growth = metric_vals.pct_change().dropna()
    if metric_growth.empty:
        return {}

    growth_factors = 1 + metric_growth
    product = growth_factors.prod()

    if isinstance(product, float):
        annual_metric_growth = product - 1

        return {
            'ticker': ticker,
            'growth': annual_metric_growth
        }
    else:
        return {}

def eps_growth(ticker):
    return

