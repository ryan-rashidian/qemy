import pandas as pd
from qemy.data.api_tiingo import StockMarket
from qemy.utils.parse_arg import parse_args

#================================== TIINGO ===================================#

def quote(arg):
    try:
        ticker = arg.strip().upper()
        if isinstance(ticker, str):
            data = StockMarket().get_quote(tickers=ticker)
            if data and ticker in data:
                quote_data = data[ticker]
                quote = quote_data.get('last') or quote_data.get('tngoLast') or quote_data.get('mid')
                if quote is not None:
                    print(f"{ticker}: {quote}")
            else:
                print(f"Could note fetch data for {ticker}, please try another ticker.")
        else:
            print("For valid syntax Try: quote <TICKER>")
    except Exception as e:
        print(f"Error:\n{e}")

def price(arg):
    period, ticker = parse_args(arg_str=arg, expected_args=['period', 'ticker'], prog_name='price')
    if isinstance(period, str) and isinstance(ticker, str):
        print(f"Fetching price info for: {ticker}...")
        data = StockMarket().get_prices(ticker=ticker, period=period)
        if data is None:
            print('Could not fetch data, please try another ticker or period.')
            return
        try:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            print(df)
        except Exception as e:
            print(f"Error:\n{e}")
    else:
        print('For valid syntax, Try: price AAPL -p 3M')

