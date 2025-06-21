import pandas as pd
from qemy.data.api_tiingo import StockMarket
from qemy.utils.parse_arg import parse_args_cli, check_help
from qemy.cli.cli_helper import print_help_table

#================================== TIINGO ===================================#

def quote(arg):
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" quote ", [
            ("Info:", "Fetches Price Quote data for given ticker"),
            ("Usage:", "quote <TICKER>"),
            ("Example:", "quote aapl\n"),
        ])
    ):
        return

    core_args, plugin_kwargs, other_args = parse_args_cli(
        arg_str=arg, 
        expected_args=['ticker'], 
        prog_name='quote', 
    )

    if plugin_kwargs or other_args:
        print(f"Unexpected command: {other_args} {plugin_kwargs}")
        return

    ticker, = core_args

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
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" price ", [
            ("Info:", "Fetches Price data for given ticker"),
            ("Usage:", "price <TICKER> -p <PERIOD>"),
            ("Example:", "price aapl -p 1y\n"),
        ])
    ):
        return
    core_args, plugin_kwargs, other_args = parse_args_cli(
        arg_str=arg, 
        expected_args=['period', 'ticker'], 
        prog_name='price', 
    )

    if plugin_kwargs or other_args:
        print(f"Unexpected command: {other_args} {plugin_kwargs}")
        return

    period, ticker = core_args

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

