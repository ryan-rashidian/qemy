import os

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

    def run(self):

        while True:
            user_input = input("qemy>wl> ").upper()

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
            elif user_input in ('EXIT', 'Q'):
                save_watchlist = input("Save changes? (yes/no): ")
                if save_watchlist == 'yes':
                    print("Exiting and saving Watchlist.")
                    return self.tickers
                else:
                    print('Exiting without saving Watchlist.')
                    return None
            else:
                print('Unknown command.')

