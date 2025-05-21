import cmd
import os
import pandas as pd
from backend.fetch import api_tiingo as tiingo
from backend.fetch import api_fmp as fmp
from frontend.utils import parse_args

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

class QemyShell(cmd.Cmd):
    intro = "Welcome to Qemy. Type help or ? to list commands.\n"
    prompt = "qemy> "
#==============================================================================#
    def do_price(self, arg):
        def define_args(parser):
            parser.add_argument('ticker', help='stock ticker symbol')
            parser.add_argument('-p', '--period', default='1W', help='period (e.g. 5D, 3M, 1Y)')

        args = parse_args(arg, define_args, prog_name='price')
        if not args:
            print('For valid syntax, Try: price AAPL -p 3M')
            return

        ticker = args.ticker.upper()
        period = args.period
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
    def help_price(self):
        print('Fetches daily closing prices for given ticker.')
        print('Usage: price <TICKER> -p <PERIOD>')
        print('Example: price AAPL -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#==============================================================================#
    def do_dcf(self, arg):
        ticker = arg.strip().upper()
        print(f"Fetching discounted cash flow for {ticker}...")
        try:
            data = [fmp.get_dcf(ticker)]
            df = pd.DataFrame(data).T
            print(df)
        except:
            print('Could not fetch data, please try another ticker.')
    def help_dcf(self):
        print('Fetches current discounted cash flow for given ticker.')
        print('Usage: dcf <TICKER>')
        print('Example: dcf AAPL')
#==============================================================================#
    def do_profile(self, arg):
        ticker = arg.strip().upper()
        print(f"Fetching profile for {ticker}...")
        try:
            data = [fmp.get_profile(ticker)]
            df = pd.DataFrame(data).T
            print(df)
        except:
            print('Could not fetch data, please try another ticker.')
    def help_profile(self):
        print('Fetches profile for a given ticker. Shows basic info about the company.')
        print('Usage: profile <TICKER>')
        print('Example: profile AAPL')
#==============================================================================#
    def do_ratios(self, arg):
        ticker = arg.strip().upper()
        print(f"Fetching ratios for {ticker}...")
        try:
            data = [fmp.get_ratios(ticker)]
            df = pd.DataFrame(data).T
            print(df)
        except:
            print('Could not fetch data, please try another ticker.')
    def help_ratios(self):
        print('Fetches list of ratios for given ticker.')
        print('Usage: ratios <TICKER>')
        print('Example: ratios AAPL')
#==============================================================================#
    def do_balance(self, arg):
        ticker = arg.strip().upper()
        print(f"Fetching balance sheet for {ticker}...")
        try:
            data = [fmp.get_balance(ticker)]
            df = pd.DataFrame(data).T
            print(df)
        except:
            print('Could not fetch data, please try another ticker.')
    def help_balance(self):
        print('Fetches latest balance sheet for given ticker.')
        print('Usage: balance <TICKER>')
        print('Example: balance AAPL')
#==============================================================================#
    def do_metrics(self, arg):
        ticker = arg.strip().upper()
        print(f"Fetching metrics for {ticker}...")
        try:
            data = [fmp.get_metrics(ticker)]
            df = pd.DataFrame(data).T
            print(df)
        except:
            print('Could not fetch data, please try another ticker.')
    def help_metrics(self):
        print('Fetches list of the latest metrics for given ticker.')
        print('Usage: metrics <TICKER>')
        print('Example: metrics AAPL')
#==============================================================================#
    def do_cf(self, arg):
        ticker = arg.strip().upper()
        print(f"Fetching cash flow statement for {ticker}...")
        try:
            data = [fmp.get_cf(ticker)]
            df = pd.DataFrame(data).T
            print(df)
        except:
            print('Could not fetch data, please try another ticker.')
    def help_cf(self):
        print('Fetches latest cash flow statement for given ticker.')
        print('Usage: cf <TICKER>')
        print('Example: cf AAPL')
#==============================================================================#
    def do_income(self, arg):
        ticker = arg.strip().upper()
        print(f"Fetching income statement for {ticker}...")
        try:
            data = [fmp.get_income(ticker)]
            df = pd.DataFrame(data).T
            print(df)
        except:
            print('Could not fetch data, please try another ticker.')
    def help_income(self):
        print('Fetches latest income statement for given ticker.')
        print('Usage: income <TICKER>')
        print('Example: income AAPL')
#==============================================================================#
    def do_52week(self, arg):
        ticker = arg.strip().upper()
        print(f"Fetching 52 week high/low for {ticker}...")
        try:
            data = [fmp.get_52_week(ticker)]
            df = pd.DataFrame(data).T
            print(df)
        except:
            print('Could not fetch data, please try another ticker.')
    def help_52week(self):
        print('Fetches 52-week high and low for given ticker.')
        print('Usage: 52week <TICKER>')
        print('Example: 52week AAPL')
#==============================================================================#
    def do_ev(self, arg):
        ticker = arg.strip().upper()
        print(f"Fetching enterprise value for {ticker}...")
        try:
            data = [fmp.get_ev(ticker)]
            df = pd.DataFrame(data).T
            print(df)
        except:
            print('Could not fetch data, please try another ticker.')
    def help_ev(self):
        print('Fetches the enterprise value for given ticker.')
        print('Usage: ev <TICKER>')
        print('Example: ev AAPL')
#==============================================================================#
    def do_clear(self, arg):
        arg = arg # supress lsp
        os.system('clear')
#==============================================================================#
    def do_exit(self, arg):
        arg = arg # supress lsp
        print("Exiting... Goodbye!")
        return True
#==============================================================================#
if __name__ == '__main__':
    QemyShell().cmdloop()
