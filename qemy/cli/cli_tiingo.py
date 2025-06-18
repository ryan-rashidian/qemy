import pandas as pd
from qemy.data.api_tiingo import StockMarket
from qemy.utils.parse_arg import parse_args_help
from qemy.cli.cli_helper import print_help_table

#================================== TIINGO ===================================#

def quote(arg):
    parse_result = parse_args_help(
        arg_str=arg, 
        expected_args=['ticker', 'help'], 
        prog_name='quote', 
        help_func=lambda: print_help_table(" quote ", [
            ("Info:", "Fetches Price Quote data for given ticker"),
            ("Usage:", "quote <TICKER>\n"),
        ])
    )
    if parse_result == '__HELP__':
        return
    if not isinstance(parse_result, tuple):
        raise ValueError("Unexpected parsing result")

    ticker, _ = parse_result

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

def price(arg):
    parse_result = parse_args_help(
        arg_str=arg, 
        expected_args=['period', 'ticker', 'help'], 
        prog_name='price', 
        help_func=lambda: print_help_table(" price ", [
            ("Info:", "Fetches Price data for given ticker"),
            ("Usage:", "price <TICKER> -p <PERIOD>\n"),
        ])
    )
    if parse_result == '__HELP__':
        return
    if not isinstance(parse_result, tuple):
        raise ValueError("Unexpected parsing result")

    period, ticker, _ = parse_result

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

