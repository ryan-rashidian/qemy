"""Discounted Cash Flow Model."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from qemy.core.metrics import get_fcf, get_netdebt
from qemy.data import EDGARClient
from qemy.exceptions import ModelError


def calc_dcf(
    ticker: str,
    discount_rate: float = 0.09,
    growth_rate: float = 0.02
) -> dict:
    """Calculate 'Discounted Cash Flow' metrics.

    Args:
        ticker (str): Company ticker symbol
        discount_rate (float): Discount rate
        growth_rate (float): Perpetuity growth rate

    Returns:
        dict: Contains DCF metric data for given ticker

    Raises:
        ModelError: If input data is missing for calculations
    """
    try:
        shares_df = EDGARClient(ticker).get_concept(concept='shares')
        shares = shares_df['val'].iloc[-1]
        fcf_df = get_fcf(ticker, quarters=20)
        netdebt = get_netdebt(ticker)
    except Exception as e:
        raise ModelError(f"DCF for {ticker} Error: missing data") from e

    # Calculate 4-quater rolling average for FCF
    fcf_rolling_win = fcf_df['val'].rolling(window=4)
    fcf_avg_4q = pd.Series(fcf_rolling_win.mean()).dropna().values

    # Fit model using time steps (quarters) and historical FCF values
    x_features = np.arange(len(fcf_avg_4q)).reshape(-1, 1)
    y_target = fcf_avg_4q
    model = LinearRegression().fit(x_features, y_target)
    r_squared = model.score(x_features, y_target)

    # Predict future FCF values using linear trend
    x_features_predict = np.arange(
        len(fcf_avg_4q),
        len(fcf_avg_4q) + 20
    ).reshape(-1, 1)
    fcf_forecast = model.predict(x_features_predict)
    fcf_forecast = np.clip(fcf_forecast, 0, None)

    # Calculate 'Discounted Free Cash Flow'
    q_discount_rate = discount_rate / 4
    quarters = np.arange(1, 21)
    discount_factors = 1 / (1 + q_discount_rate) ** quarters
    discounted_fcf = fcf_forecast * discount_factors

    # Calculate 'Terminal Value' using Gordon Growth Model
    # Terminal Value = fcf_last * (1 + g) / (r - g)
    # where:
    #   fcf_last = last forecasted FCF
    #   g = Perpetuity Growth Rate
    #   r = Discount Rate (typically WACC)
    g = growth_rate
    r = discount_rate
    fcf_last = fcf_forecast[-1]
    terminal_value = (fcf_last * (1 + g)) / (r - g)

    # Discount 'Terminal Value' back to present value
    n = len(fcf_forecast)
    discounted_tv = terminal_value / ((1 + q_discount_rate) ** n)

    # Calculate IVPS - 'Intrinsic Value Per Share'
    enterprise_value = np.sum(discounted_fcf) + discounted_tv
    equity_value = enterprise_value - netdebt
    ivps = max(0, equity_value / shares)

    return {
        'fit': r_squared,
        'ev': equity_value,
        'ivps': ivps
    }

