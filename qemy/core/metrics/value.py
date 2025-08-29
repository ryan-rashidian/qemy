import pandas as pd

from qemy.data import EDGARClient, SECFiles, TiingoClient


def ratio_pe(ticker):
    eps_concept: SECFiles = EDGARClient(ticker).get_concept(
        concept='epsd',
        quarters=20
    )
    eps_df: pd.DataFrame = eps_concept.data

    if eps_df is not None:
        def _get_val(pos: int) -> float:
            return eps_df.iloc[pos]['val'] if 0 <= pos < len(eps_df) else 0

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
                ttm_eps = max_eps

            elif n_quarters == 1:
                q1 = after_cumulative_df.iloc[0]['val']
                q1_last_year = _get_val(cumulative_pos - 3)

                ttm_eps = max_eps + q1 - q1_last_year

            elif n_quarters == 2:
                q1 = after_cumulative_df.iloc[0]['val']
                q2 = after_cumulative_df.iloc[1]['val']
                q1_last_year = _get_val(cumulative_pos - 3)
                q2_last_year = _get_val(cumulative_pos - 2)

                ttm_eps = (
                    max_eps
                    + q1 + q2
                    - q1_last_year
                    - q2_last_year
                )

            elif n_quarters == 3:
                q1 = after_cumulative_df.iloc[0]['val']
                q2 = after_cumulative_df.iloc[1]['val']
                q3 = after_cumulative_df.iloc[2]['val']
                q1_last_year = _get_val(cumulative_pos - 3)
                q2_last_year = _get_val(cumulative_pos - 2)
                q3_last_year = _get_val(cumulative_pos - 1)

                ttm_eps = (
                    max_eps
                    + q1 + q2 + q3
                    - q1_last_year
                    - q2_last_year
                    - q3_last_year
                )

        else:
            ttm_eps = eps_1y_df.mean()

        if ttm_eps is None or ttm_eps == 0:
            print("eps not found")
            return {}

    price_df = TiingoClient(ticker=ticker).get_prices(period='2W')
    if price_df.empty:
        return {}

    price = price_df.iloc[-1]['adjClose']

    if price:
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
    equity_concept: SECFiles = EDGARClient(ticker).get_concept(
        concept='equity',
        quarters=4
    )
    equity_df: pd.DataFrame = equity_concept.data

    book_value = equity_df.iloc[-1]['val']

    shares_concept: SECFiles = EDGARClient(ticker).get_concept(
        concept='shares',
        quarters=4
    )
    shares_df: pd.DataFrame = shares_concept.data

    shares_outstanding = shares_df.iloc[-1]['val']

    bvps = round(book_value / shares_outstanding, 2)

    price_df = TiingoClient(ticker).get_prices(period='2W')
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

def ratio_ps():
    return

def ratio_enterprise_multiple():
    return

def market_cap():
    return

