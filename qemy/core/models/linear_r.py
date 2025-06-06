import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from qemy.data.api_tiingo import get_tiingo_prices

def linear_r(ticker, period):
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
        x_ind = np.array(returns['SPY']).reshape(-1, 1) 
        y_dep = np.array(returns[ticker])

        model = LinearRegression()
        model.fit(X=x_ind, y=y_dep)
        alpha = model.intercept_
        beta = model.coef_[0]
        return x_ind, y_dep, alpha, beta, model
    except Exception as e:
        print(f"core/models/linear_r.py Exception ERROR:\n{e}")
        return None, None, None, None, None 

