"""Score-based Metrics."""

from qemy.core.metrics import get_gross_margin, ratio_current, ratio_roa
from qemy.data import EDGARClient


def altman_z():
    return

def beneish_m():
    return

def piotroski_f(ticker: str) -> dict:
    """Calculate Piotroski f-score for given ticker.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: With 'piotroski_f' key and corresponding value
    """
    client = EDGARClient(ticker)

    # Section: Profitability
    try:
        net_inc_df = client.get_concept(concept='netinc')
        net_inc = net_inc_df['val'].iloc[-1]
    except Exception:
        net_inc = 0.0
    fscore_net_inc = 1.0 if net_inc > 0.0 else 0.0

    try:
        ocf_df = client.get_concept(concept='ocf')
        ocf = ocf_df['val'].iloc[-1]
    except Exception:
        ocf = 0.0
    fscore_ocf = 1.0 if ocf > 0.0 else 0.0
    fscore_accruals = 1.0 if ocf > net_inc else 0.0

    roa_df = ratio_roa(ticker)
    current_roa = roa_df['val'].iloc[-1]
    previous_roa = roa_df['val'].iloc[-5]
    fscore_roa = 1.0 if current_roa > previous_roa else 0.0

    # Section: Leverage, Liquidity
    try:
        ldebt_df = client.get_concept(concept='ldebt')
        current_ldebt = ldebt_df['val'].iloc[-1]
        previous_ldebt = ldebt_df['val'].iloc[-5]
        fscore_ldebt = 1.0 if current_ldebt < previous_ldebt else 0.0
    except Exception:
        fscore_ldebt = 1.0

    ##### placeholder for current ratio after enhancements
    current_ratio_df = ratio_current(ticker)
    current_cr = current_ratio_df['val'].iloc[-1]
    previous_cr = current_ratio_df['val'].iloc[-5]
    fscore_cratio = 1.0 if current_cr > previous_cr else 0.0

    try:
        shares_df = client.get_concept(concept='shares')
        current_shares = shares_df['val'].iloc[-1]
        previous_shares = shares_df['val'].iloc[-5]
        fscore_shares = 1.0 if current_shares <= previous_shares else 0.0
    except Exception:
        fscore_shares = 0.0

    gross_margin_df = get_gross_margin(ticker)
    current_gmargin = gross_margin_df['val'].iloc[-1]
    previous_gmargin = gross_margin_df['val'].iloc[-5]
    fscore_gmargin = 1.0 if current_gmargin > previous_gmargin else 0.0

    try:
        rev_df = client.get_concept('revenue')
        revenue = rev_df['val'].iloc[-1]
        revenue_prev = rev_df['val'].iloc[-5]

        assets_df = client.get_concept('assets')
        assets_current = assets_df['val'].iloc[-1]
        assets_previous = assets_df['val'].iloc[-5]
        assets_pprev = assets_df['val'].iloc[-9]
        avg_assets = (assets_current + assets_previous) / 2.0
        avg_assets_prev = (assets_previous + assets_pprev) / 2.0

        at_current = revenue / avg_assets if avg_assets else 0
        at_previous = revenue_prev / avg_assets_prev if avg_assets_prev else 0

        fscore_asset_turnover = 1.0 if at_current > at_previous else 0.0
    except Exception:
        fscore_asset_turnover = 0.0

    fscore_total = sum([
        fscore_net_inc,
        fscore_ocf,
        fscore_accruals,
        fscore_roa,
        fscore_ldebt,
        fscore_cratio,
        fscore_shares,
        fscore_gmargin,
        fscore_asset_turnover
    ])

    return {
        'ticker': ticker,
        'piotroski_f': fscore_total
    }

