from qemy.data import TiingoClient
from qemy.data import EDGARClient

def ratio_pe(ticker):
    eps_df = EDGARClient(ticker=ticker).get_concept(concept='epsd', quarters=20)

    if not eps_df is None:
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
                #print("0")
                ttm_eps = max_eps

            elif n_quarters == 1:
                #print("1")
                q1 = after_cumulative_df.iloc[0]['val']
                q1_last_year = eps_df.iloc[cumulative_pos - 3]['val'] if cumulative_pos - 3 >= 0 else 0
                ttm_eps = max_eps + q1 - q1_last_year

            elif n_quarters == 2:
                #print("2")
                q1 = after_cumulative_df.iloc[0]['val']
                q2 = after_cumulative_df.iloc[1]['val']
                q1_last_year = eps_df.iloc[cumulative_pos - 3]['val'] if cumulative_pos - 3 >= 0 else 0
                q2_last_year = eps_df.iloc[cumulative_pos - 2]['val'] if cumulative_pos - 2 >= 0 else 0
                ttm_eps = max_eps + q1 + q2 - q1_last_year - q2_last_year

            elif n_quarters == 3:
                #print("3")
                q1 = after_cumulative_df.iloc[0]['val']
                q2 = after_cumulative_df.iloc[1]['val']
                q3 = after_cumulative_df.iloc[2]['val']
                q1_last_year = eps_df.iloc[cumulative_pos - 3]['val'] if cumulative_pos - 3 >= 0 else 0
                q2_last_year = eps_df.iloc[cumulative_pos - 2]['val'] if cumulative_pos - 2 >= 0 else 0
                q3_last_year = eps_df.iloc[cumulative_pos - 1]['val'] if cumulative_pos - 1 >= 0 else 0
                ttm_eps = max_eps + q1 + q2 + q3 - q1_last_year - q2_last_year - q3_last_year

        else:
            #print("else")
            ttm_eps = eps_1y_df.mean()

        if ttm_eps is None or ttm_eps == 0:
            print("eps not found")
            return {}

    else:
        print("No filing data")
        return {}

    price_df = TiingoClient().get_prices(ticker=ticker)
    if price_df.empty:
        return {}

    price = price_df.iloc[-1]['adjClose']

    if price and ttm_eps:
        pe_ratio = round(price / ttm_eps, 2)

        if pe_ratio >= 200:
            ttm_eps = eps_1y_df.sum()
            pe_ratio = round(price / ttm_eps, 2)

        return {
            'ticker': ticker,
            'price': price,
            'ttm_eps': ttm_eps,
            'pe': pe_ratio
        }

    else:
        print("No price data")
        return {}

def ratio_pb(ticker):
    equity_df = EDGARClient(ticker=ticker).get_concept(concept='equity', quarters=4)
    if equity_df is None:
        return {}
    book_value = equity_df.iloc[-1]['val']

    shares_df = EDGARClient(ticker=ticker).get_concept(concept='shares', quarters=4)
    if shares_df is None:
        return {}
    shares_outstanding = shares_df.iloc[-1]['val']

    bvps = round(book_value / shares_outstanding, 2)

    price_df = TiingoClient().get_prices(ticker=ticker)
    if price_df.empty:
        return {}

    price_per_share = price_df.iloc[-1]['adjClose']
    pb_ratio = round(price_per_share / bvps, 2)

    return {
        'ticker': ticker,
        'price': price_per_share,
        'bvps': bvps,
        'pb': pb_ratio 
    }

def ratio_roe():
    return

def ratio_ev_ebitda():
    return

