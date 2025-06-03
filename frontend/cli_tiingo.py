import pandas as pd
from backend.fetch import api_tiingo as tiingo
from . import parse_arg
#=============================================================================#
################################## PRICE ######################################
#=============================================================================#
def price(arg):
    period, ticker = parse_arg.parse_arg_p_t(arg=arg, name='price')
    if isinstance(period, str) and isinstance(ticker, str):
        print(f"Fetching price info for: {ticker}...")
        data = tiingo.get_tiingo_prices(ticker=ticker, period=period)
        if data is None:
            print('Could not fetch data, please try another ticker or period.')
            return
        try:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            print(df)
        except Exception as e:
            print('Failed to parse data: ', e)
    else:
        print('For valid syntax, Try: price AAPL -p 3M')

