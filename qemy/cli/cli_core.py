import os
from numbers import Number
from qemy.utils.utils_cli import save_to_csv
from qemy.utils.parse_arg import parse_args

#================================== CORE =====================================#

class WatchListManager:
    def __init__(self, ticker_list):
        self.tickers = ticker_list

    def add(self, ticker):
        if ticker not in self.tickers:
            self.tickers.append(ticker)
            print(f"Adding: {ticker}")
        else:
            print(f"{ticker} is already in the list.")

    def remove(self, ticker):
        if ticker in self.tickers:
            self.tickers.remove(ticker)
            print(f"Removing: {ticker}")
        else:
            print(f"{ticker} not found in the list.")

    def show(self):
        print("Current tickers:")
        for t in self.tickers:
            print(f"- {t}")

    def help(self):
        print("Watchlist manager:\n- 'add <TICKER>'\n- 'remove <Ticker>'\n- 'show'\n- 'clear'\n- 'exit'\n- 'help'")

    def run(self):
        print("Watchlist manager:\n- type 'help' to list commands.")

        while True:
            user_input = input("qemy>watchlist> ").upper()

            if user_input.startswith('ADD'):
                ticker = user_input.split()[1:]
                ticker = [s.strip() for s in ticker]
                for t in ticker:
                    self.add(t)
            elif user_input.startswith('REMOVE'):
                ticker = user_input.split()[1:]
                ticker = [s.strip() for s in ticker]
                for t in ticker:
                    self.remove(t)
            elif user_input == 'SHOW':
                self.show()
            elif user_input == 'CLEAR':
                os.system('clear')
            elif user_input == 'HELP':
                self.help()
            elif user_input in ('EXIT', 'Q'):
                save_watchlist = input("Save changes? (yes/no): ")
                if save_watchlist == 'yes':
                    print("Exiting and saving current watchlist.")
                    return self.tickers
                else:
                    print('Exiting watchlist editor.')
                    return None
            else:
                print('Unknown command.')

def table(arg, ticker_df):
    save_state, = parse_args(arg_str=arg, expected_args=['save'], prog_name='table')
    if isinstance(save_state, str):
        try:
            if save_state:
                save_to_csv(df=ticker_df)
                print("File saved...\n /qemy/exports/tables/")
            else:
                print('Filings:')
                print(ticker_df.to_string(justify='left', formatters={
                    col: (lambda x: f"{x:,}" if isinstance(x, Number) else x)
                    for col in ticker_df.columns
                }))
        except Exception as e:
            print(f"Could not fetch/save table. ERROR:\n{e}")
    else:
        print("For valid syntax, Try: table -s yes")
