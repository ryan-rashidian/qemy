from qemy.data import TiingoClient

from .._parse_args import check_help, parse_args_cli
from ..core.helper import print_help_table

# === TIINGO ===

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

    try:
        core_args, plugin_kwargs, other_args = parse_args_cli(
            arg_str=arg,
            expected_args=['ticker'],
            prog_name='quote',
        )
    except Exception as e:
        print(e)
        return

    if plugin_kwargs or other_args:
        print(f"Unexpected command: {other_args} {plugin_kwargs}")
        return

    ticker, = core_args

    if isinstance(ticker, str):
        try:
            data = TiingoClient(ticker=ticker).get_quote()
            if data and ticker in data:
                quote_data = data[ticker]
                quote = (
                    quote_data.get('last')
                    or quote_data.get('tngoLast')
                    or quote_data.get('mid'))
                if quote is not None:
                    print(f"{ticker}: {quote}")
            else:
                print(f"Could note fetch data for {ticker}.")

        except Exception as e:
            print(e)
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

    try:
        core_args, plugin_kwargs, other_args = parse_args_cli(
            arg_str=arg,
            expected_args=['period', 'ticker'],
            prog_name='price',
        )
    except Exception as e:
        print(e)
        return

    if plugin_kwargs or other_args:
        print(f"Unexpected command: {other_args} {plugin_kwargs}")
        return

    period, ticker = core_args

    if isinstance(period, str) and isinstance(ticker, str):
        print(f"Fetching price info for: {ticker}...")

        try:
            price_df = TiingoClient(ticker=ticker).get_prices(period=period)
            formatted_df = price_df.reset_index()
            formatted_df['date'] = formatted_df['date'].dt.strftime('%Y-%m-%d')
            print(formatted_df)

        except Exception as e:
            print(e)

    else:
        print('For valid syntax, Try: price AAPL -p 3M')

