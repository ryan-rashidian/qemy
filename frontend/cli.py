import cmd
import os
import pandas as pd
from backend.fetch import api_tiingo as tiingo
from backend.fetch import api_fmp as fmp

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

class QemyShell(cmd.Cmd):
    intro = "Welcome to Qemy. Type help or ? to list commands.\n"
    prompt = "qemy> "

    def do_price(self, arg):
        parts = arg.strip().split()
        if len(parts) != 2:
            print('Usage: price <TICKER> <PERIOD>')
            return

        ticker, period = parts
        print(f"Fetching price info for: {ticker}...")
        data = tiingo.get_tiingo_prices(ticker=ticker, period=period)
        if data is None:
            print('Could not fetch data, Please try another ticker or period')
            return
        try:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            print(df)
        except Exception as e:
            print('Failed to parse data: ', e)

    def do_dcf(self, arg):
        print(f"Fetching latest SEC filing for {arg}...")
        df = pd.DataFrame([fmp.get_dcf(arg)])
        print(df)

    def do_profile(self, arg):
        print(f"Fetching profile for {arg}...")
        df = pd.DataFrame([fmp.get_profile(arg)]).T
        print(df)

    def do_ratios(self, arg):
        print(f"Fetching ratios for {arg}...")
        df = pd.DataFrame([fmp.get_ratios(arg)]).T
        print(df)

    def do_balance(self, arg):
        print(f"Fetching balance sheet for {arg}...")
        df = pd.DataFrame([fmp.get_balance(arg)]).T
        print(df)

    def do_metrics(self, arg):
        print(f"Fetching metrics for {arg}...")
        df = pd.DataFrame([fmp.get_metrics(arg)]).T
        print(df)

    def do_cf(self, arg):
        print(f"Fetching cash flow statement for {arg}...")
        df = pd.DataFrame([fmp.get_cf(arg)]).T
        print(df)

    def do_income(self, arg):
        print(f"Fetching income statement for {arg}...")
        df = pd.DataFrame([fmp.get_income(arg)]).T
        print(df)

    def do_52week(self, arg):
        print(f"Fetching 52 week high/low for {arg}...")
        df = pd.DataFrame([fmp.get_52_week(arg)]).T
        print(df)

    def do_ev(self, arg):
        print(f"Fetching enterprise value for {arg}...")
        df = pd.DataFrame([fmp.get_ev(arg)]).T
        print(df)

    def do_clear(self, arg):
        arg = arg # supress lsp
        os.system('clear')

    def do_exit(self, arg):
        arg = arg # supress lsp
        print("Exiting... Goodbye!")
        return True

if __name__ == '__main__':
    QemyShell().cmdloop()
