import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from qemy.data.api_tiingo import get_tiingo_prices

def linear_r(ticker, period, **_):
    try:
        ind_data = get_tiingo_prices(ticker=ticker, period=period)
        dep_data = get_tiingo_prices(ticker='SPY', period=period)

        ind_df, dep_df = pd.DataFrame(ind_data), pd.DataFrame(dep_data)
        ind_df.set_index('date', inplace=True)
        ind_df.index = pd.to_datetime(ind_df.index)
        dep_df.set_index('date', inplace=True)
        dep_df.index = pd.to_datetime(dep_df.index)
        data = pd.DataFrame({
            ticker: ind_df['close'], 
            'SPY': dep_df['close']
        }).dropna()
        returns = data.pct_change().dropna()

        x_axis = np.array(returns['SPY']).reshape(-1, 1) 
        y_axis = np.array(returns[ticker])

        model = LinearRegression()
        model.fit(X=x_axis, y=y_axis)
        alpha = model.intercept_
        beta = model.coef_[0]

        return {
            "text": {
                "Alpha": alpha,
                "Beta": beta,
            },
            "plot": {
                "title": f"Linear Regression fit for {ticker} and SPY returns",
                "x_axis": x_axis,
                "y_axis": y_axis,
            },
        }

    except Exception as e:
        print(f"core/models/linear_r.py Exception ERROR:\n{e}")
        return None 

