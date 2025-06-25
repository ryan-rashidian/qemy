import pandas as pd
from qemy.data.api_tiingo import StockMarket
from qemy.data.api_edgar import SEC_Filings

def ratio_pe(ticker):
    eps_df = SEC_Filings(ticker=ticker).get_metric_history(key='eps')

    if isinstance(eps_df, pd.DataFrame):
        ttm_eps = None

        eps_1y_df = eps_df['val'].tail(4).copy()
        sample_df = eps_df['val'].tail(6).copy()
        max_eps = eps_1y_df.max()
        mean_eps_others = sample_df[sample_df != max_eps].mean()

        if max_eps >= 1.9 * mean_eps_others:
            cumulative_idx = eps_1y_df.idxmax()
            cumulative_pos = eps_df.index.get_indexer_for([cumulative_idx])[0]
            after_cumulative_df = eps_df.iloc[cumulative_pos + 1:]
            n_quarters = len(after_cumulative_df)

            if n_quarters == 0:
                print("0")
                ttm_eps = max_eps

            elif n_quarters == 1:
                print("1")
                q1 = after_cumulative_df.iloc[0]['val']
                q1_last_year = eps_df.iloc[cumulative_pos - 3]['val'] if cumulative_pos - 3 >= 0 else 0
                ttm_eps = max_eps + q1 - q1_last_year

            elif n_quarters == 2:
                print("2")
                q1 = after_cumulative_df.iloc[0]['val']
                q2 = after_cumulative_df.iloc[1]['val']
                q1_last_year = eps_df.iloc[cumulative_pos - 3]['val'] if cumulative_pos - 3 >= 0 else 0
                q2_last_year = eps_df.iloc[cumulative_pos - 2]['val'] if cumulative_pos - 2 >= 0 else 0
                ttm_eps = max_eps + q1 + q2 - q1_last_year - q2_last_year

            elif n_quarters == 3:
                print("3")
                q1 = after_cumulative_df.iloc[0]['val']
                q2 = after_cumulative_df.iloc[1]['val']
                q3 = after_cumulative_df.iloc[2]['val']
                q1_last_year = eps_df.iloc[cumulative_pos - 3]['val'] if cumulative_pos - 3 >= 0 else 0
                q2_last_year = eps_df.iloc[cumulative_pos - 2]['val'] if cumulative_pos - 2 >= 0 else 0
                q3_last_year = eps_df.iloc[cumulative_pos - 1]['val'] if cumulative_pos - 1 >= 0 else 0
                ttm_eps = max_eps + q1 + q2 + q3 - q1_last_year - q2_last_year - q3_last_year

        else:
            print("else")
            ttm_eps = eps_1y_df.mean()

        if ttm_eps is None or ttm_eps == 0:
            return "N/A 1"

    else:
        return "N/A 2"

    price_data = StockMarket().get_prices(ticker=ticker)

    try: 
        price_df = pd.DataFrame(price_data)
        price = price_df.iloc[-1]['close']
    except:
        return "N/A 3"

    if price and ttm_eps:
        pe_ratio = round(price / ttm_eps, 2)
        if pe_ratio >= 200:
            ttm_eps = eps_1y_df.sum()
            pe_ratio = round(price / ttm_eps, 2)
        return (
            f"{ticker}\n"
            f"Price: {price:.2f}\n"
            f"TTM EPS: {ttm_eps:.2f}\n"
            f"P/E Ratio: {pe_ratio}"
        )

def ratio_pb(ticker):
    equity_df = SEC_Filings(ticker=ticker).get_metric_history(key='equity')
    book_value = equity_df.iloc[-1]['val']

    shares_df = SEC_Filings(ticker=ticker).get_metric_history(key='shares')
    shares_outstanding = shares_df.iloc[-1]['val']

    bvps = round(book_value / shares_outstanding, 2)

    try: 
        price_data = StockMarket().get_prices(ticker=ticker)
        price_df = pd.DataFrame(price_data)
        price_per_share = price_df.iloc[-1]['close']
    except:
        return f"No price data found for: {ticker}"

    pb_ratio = round(price_per_share / bvps, 2)
    return (
        f"{ticker}\n"
        f"Price: {price_per_share}\n"
        f"BVPS: {bvps}\n"
        f"P/B Ratio: {pb_ratio}"
    )

def ratio_roe():
    return

def ratio_ev_ebitda():
    return

def ratio_sharpe():
    return

