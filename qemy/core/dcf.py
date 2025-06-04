import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from data.api_edgar import SEC_Filings

def get_dcf_eval(ticker):
    df, shares_outstanding = SEC_Filings(ticker=ticker).get_dcf_metrics()

    if isinstance(df, pd.DataFrame) and shares_outstanding is not None:
        fcf = df['fcf'].values
        x_axis = np.arange(len(fcf)).reshape(-1, 1)
        y_axis = fcf
        model = LinearRegression().fit(X=x_axis, y=y_axis)
        future_x = np.arange(len(fcf), len(fcf) + 20).reshape(-1, 1)
        fcf_forecast = model.predict(future_x)

        discount_rate = 0.09 / 4
        quarters = np.arange(1, 21)
        discount_factors = 1 / (1 + discount_rate) ** quarters
        discounted_fcf = fcf_forecast * discount_factors
        g = 0.02
        r = 0.09
        fcf_last = fcf_forecast[-1]
        terminal_value = (fcf_last * (1 + g)) / (r - g)
        n = len(fcf_forecast)
        discounted_tv = terminal_value / ((1 + r) ** n)

        enterprise_value = np.sum(discounted_fcf) + discounted_tv
        intrinsic_value_per_share = enterprise_value / shares_outstanding
        print(f"Enterprise Value: {enterprise_value}")
        print(f"Inrinsic Value Per-Share: {intrinsic_value_per_share}")
    else:
        print(f"Error\n{df}\nShares outstanding: {shares_outstanding}")

