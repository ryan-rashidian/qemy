import os

#================================== CORE =====================================#

class SessionManager:
    def __init__(self):
        self.tickers = []

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

    def view(self):
        print("Current tickers:")
        for t in self.tickers:
            print(f"- {t}")

    def help(self):
        print("Session:\n- 'add <TICKER>'\n- 'remove <Ticker>'\n- 'view'\n- 'clear'\n- 'exit'\n- 'help'")

    def run(self):
        print("Session running:\n- type 'help' to list commands.")

        while True:
            user_input = input("qemy>session> ").upper()

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
            elif user_input == 'VIEW':
                self.view()
            elif user_input == 'CLEAR':
                os.system('clear')
            elif user_input == 'HELP':
                self.help()
            elif user_input == 'EXIT':
                print('Exiting current session.')
                break
            else:
                print('Unknown command.')
