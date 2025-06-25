import pandas as pd
from qemy.data.api_tiingo import StockMarket
from qemy.data.api_edgar import SEC_Filings

def ratio_pe(ticker):
    eps_df = SEC_Filings(ticker=ticker).get_metric_history(key='eps')

    if isinstance(eps_df, pd.DataFrame):
        ttm_eps = None
        eps_10k_df = eps_df[eps_df['form'] == '10-K']
        last_10k_row = eps_10k_df.iloc[-1]
        last_10k_index = eps_10k_df.index[-1]
        last_10k_pos = eps_10k_df.index.get_loc(last_10k_index)
        last_10k_pos = eps_df.index.get_indexer_for([last_10k_index])[-1]
        after_10k = eps_df.iloc[last_10k_pos + 1:]
        
        if len(after_10k) == 0:
            #print("0") # for debug
            ttm_eps = last_10k_row['val']

        elif len(after_10k) == 1:
            #print("1") # for debug
            q1 = after_10k.iloc[0]['val']
            q1_last_year = eps_df.iloc[last_10k_pos - 3]['val'] if last_10k_pos - 3 >= 0 else 0
            ttm_eps = last_10k_row['val'] + q1 - q1_last_year

        elif len(after_10k) == 2:
            #print("2") # for debug
            q1 = after_10k.iloc[0]['val']
            q2 = after_10k.iloc[1]['val']
            q1_last_year = eps_df.iloc[last_10k_pos - 3]['val'] if last_10k_pos - 3 >= 0 else 0
            q2_last_year = eps_df.iloc[last_10k_pos - 2]['val'] if last_10k_pos - 2 >= 0 else 0
            ttm_eps = last_10k_row['val'] + q1 + q2 - q1_last_year - q2_last_year

        elif len(after_10k) == 3:
            #print("3") # for debug
            q3 = after_10k.iloc[2]['val']
            q3_last_year = eps_df.iloc[last_10k_pos - 1]['val'] if last_10k_pos - 1 >= 0 else 0
            ttm_eps = last_10k_row['val'] + q3 - q3_last_year

        else:
            return "N/A 1/2"

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
        return (
            f"{ticker}\n"
            f"Price: {price:.2f}\n"
            f"TTM EPS: {ttm_eps:.2f}\n"
            f"P/E Ratio: {round(price / ttm_eps, 2)}"
        )

def ratio_pb():
    return

def ratio_roe():
    return

def ratio_ev_ebitda():
    return

def ratio_sharpe():
    return

