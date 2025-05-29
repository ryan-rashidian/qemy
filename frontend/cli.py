from utils.env_setup import setup_wizard
setup_wizard()

import cmd
import os
import pandas as pd
from backend.core import plot
from backend.core.session import SessionManager
from backend.fetch import api_tiingo as tiingo
from backend.fetch import api_fred as fred
from backend.fetch.api_edgar import SEC_Filings
from frontend.utils import parse_args

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

class QemyShell(cmd.Cmd):
    intro = "Welcome to Qemy. Type help or ? to list commands.\n"
    prompt = "qemy> "

    def __init__(self):
        metric_index = pd.Index([
            'Form', 'Filed', 'Shares Outstanding', 'Cash', 'Debt', 'Revenue',
            'COGS', 'Gross Profit', 'EBIT', 'Net Income', 'Assets', 'Liabilities', 
            'Equity', 'OpEx', 'CapEx', 'OCF', 'FCF', 'EPS', 
        ])
        super().__init__()
        self.ticker_list = []
        self.ticker_df = pd.DataFrame(index=metric_index) 
        self.ticker_df.index.name = 'Metrics:'
#=============================================================================#
################################# SESSION #####################################
#=============================================================================#
    def do_session(self, arg):
        arg = arg
        try:
            SessionManager().run()
        except Exception as e:
            print(f"Failed to load session ERROR:\n{e}")

    def help_session(self):
        print('Starts a session.')
        print('Usage: session')
        print('Example: session')
#=============================================================================#
################################### SEC #######################################
#=============================================================================#
    def do_filing(self, arg):
        ticker = arg.strip().upper()
        print(f"Fetching latest 10K/10Q filing metrics for {ticker}")
        try:
            df: pd.DataFrame = SEC_Filings(arg).get_metrics() # type: ignore
            self.ticker_df[ticker] = df[ticker]
            print(df.to_string(
                justify='left', 
                formatters={ticker: lambda x: f"{x:,}" if isinstance(x, (int, float)) else x}
            ))
        except:
            print('Could not fetch filing metrics, please try another ticker.')

    def help_filing(self):
        print('Fetches latest 10K/10Q metrics for given ticker.')
        print('Usage: filing <TICKER>')
        print('Example: filing AAPL')
#=============================================================================#
################################## FED ########################################
#=============================================================================#
    def do_rfr(self, arg):
        arg = arg
        try:
            print(fred.get_tbill_yield())
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")

    def help_rfr(self):
        print('Fetches latest 1 year T-Bill yield.')
        print('Usage: rfr')
        print('Example: rfr')
#=============================================================================#
    def do_cpi(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='cpi')
        if not args:
            print('For valid syntax, Try: cpi -p 1Y')
            return
        period = args.period

        try:
            print(fred.get_cpi_inflation(period=period))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")

    def help_cpi(self):
        print('Fetches monthly CPI data.')
        print('Usage: cpi -p <PERIOD>')
        print('Example: cpi -p 1Y')
#=============================================================================#
    def do_gdp(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='gdp')
        if not args:
            print('For valid syntax, Try: gdp -p 1Y')
            return
        period = args.period

        try:
            print(fred.get_gdp(period=period))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")

    def help_gdp(self):
        print('Fetches quarterly GDP data.')
        print('Usage: gdp -p <PERIOD>')
        print('Example: gdp -p 1Y')
#=============================================================================#
    def do_sent(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='sent')
        if not args:
            print('For valid syntax, Try: sent -p 1Y')
            return
        period = args.period

        try:
            print(fred.get_sentiment(period=period))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")

    def help_sent(self):
        print('Fetches cosumer sentiment data.')
        print('Usage: sent -p <PERIOD>')
        print('Example: sent -p 1Y')
#=============================================================================#
    def do_nfp(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='nfp')
        if not args:
            print('For valid syntax, Try: nfp -p 1Y')
            return
        period = args.period

        try:
            print(fred.get_nf_payrolls(period=period))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")

    def help_nfp(self):
        print('Fetches non-farm payroll data.')
        print('Usage: nfp -p <PERIOD>')
        print('Example: nfp -p 1Y')
#=============================================================================#
    def do_interest(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='int')
        if not args:
            print('For valid syntax, Try: interest -p 1Y')
            return
        period = args.period

        try:
            print(fred.get_interest(period=period))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")

    def help_interest(self):
        print('Fetches interest rate data.')
        print('Usage: interest -p <PERIOD>')
        print('Example: interest -p 1Y')
#=============================================================================#
    def do_jobc(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='jobc')
        if not args:
            print('For valid syntax, Try: jobc -p 1Y')
            return
        period = args.period

        try:
            print(fred.get_jobless_claims(period=period))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")

    def help_jobc(self):
        print('Fetches jobless claim data.')
        print('Usage: jobc -p <PERIOD>')
        print('Example: jobc -p 1Y')
#=============================================================================#
    def do_unem(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='unem')
        if not args:
            print('For valid syntax, Try: unem -p 1Y')
            return
        period = args.period

        try:
            print(fred.get_unemployment(period=period))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")

    def help_unem(self):
        print('Fetches unemployment data.')
        print('Usage: unem -p <PERIOD>')
        print('Example: unem -p 1Y')
#=============================================================================#
    def do_indp(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='indp')
        if not args:
            print('For valid syntax, Try: indp -p 1Y')
            return
        period = args.period

        try:
            print(fred.get_ind_prod(period=period))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")

    def help_indp(self):
        print('Fetches industrial production data.')
        print('Usage: indp -p <PERIOD>')
        print('Example: indp -p 1Y')
#=============================================================================#
    def do_comp(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='comp')
        if not args:
            print('For valid syntax, Try: comp -p 1Y')
            return
        period = args.period

        try:
            print(fred.get_composite(period=period))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")

    def help_comp(self):
        print('Fetches composite index data.')
        print('Usage: comp -p <PERIOD>')
        print('Example: comp -p 1Y')
#=============================================================================#
################################## PRICE ######################################
#=============================================================================#
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
#=============================================================================#
################################## PLOT #######################################
#=============================================================================#
    def do_plot_price(self, arg):
        def define_args(parser):
            parser.add_argument('ticker', help='stock ticker symbol')
            parser.add_argument('-p', '--period', default='1W', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='plot price')
        if not args:
            print('For valid syntax, Try: plot_price AAPL -p 3M')
            return
        ticker = args.ticker.upper()
        period = args.period

        print(f"Fetching plot chart for: {ticker} daily closing prices, log scaled...")
        try:
            plot.plot_price(ticker=ticker, period=period)
        except Exception as e:
            print(f"Could not fetch plot chart, please try another ticker. Error:\n{e}")

    def help_plot_price(self):
        print('Fetches plot chart of log scaled daily prices for given ticker.')
        print('Usage: plot_price <TICKER> -p <PERIOD>')
        print('Example: plot_price AAPL -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
    def do_plot_lr(self, arg):
        def define_args(parser):
            parser.add_argument('ticker', help='stock ticker symbol')
            parser.add_argument('-p', '--period', default='1W', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='plot lr')
        if not args:
            print('For valid syntax, Try: price_plot AAPL -p 3M')
            return
        ticker = args.ticker.upper()
        period = args.period

        print(f"Fetching plot chart for: {ticker} daily closing prices...")
        try:
            plot.plot_lr(ticker=ticker, period=period)
        except Exception as e:
            print(f"Could not fetch plot chart, please try another ticker. Error:\n{e}")

    def help_plot_lr(self):
        print('Fetches linear regression beta comparison for given ticker.')
        print('Usage: plot_lr <TICKER> -p <PERIOD>')
        print('Example: plot_lr AAPL -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
    def do_plot_cpi(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. -p 5D, --price 3M, -p 1Y)')
            parser.add_argument('-s', '--save', default='NO', help='save (e.g. -s y, --save yes)')
        args = parse_args(arg, define_args, prog_name='plot cpi')
        if not args:
            print('For valid syntax, Try: plot_cpi -p 3m -s y')
            return
        period = args.period
        save_state = args.save.upper() 

        print(f"Fetching plot chart for CPI inflation: % Change from Year Ago...")
        try:
            if save_state in ('Y', 'YES'):
                plot.plot_cpi(period=period, save=True)
            else:
                plot.plot_cpi(period=period, save=False)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")

    def help_plot_cpi(self):
        print('Fetches plot chart for CPI inflation % change from 1-Year ago.')
        print('Usage: plot_cpi -p <PERIOD>')
        print('Example: plot_cpi -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
    def do_plot_gdp(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='plot gdp')
        if not args:
            print('For valid syntax, Try: plot_gdp -p 3M')
            return
        period = args.period

        print(f"Fetching plot chart for GDP: % Change from Year Ago...")
        try:
            plot.plot_gdp(period=period)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")

    def help_plot_gdp(self):
        print('Fetches plot chart for GDP % change from 1-Year ago.')
        print('Usage: plot_gdp -p <PERIOD>')
        print('Example: plot_gdp -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
    def do_plot_sent(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='plot sent')
        if not args:
            print('For valid syntax, Try: plot_sent -p 3M')
            return
        period = args.period

        print(f"Fetching plot chart for Sentiment: % Change...")
        try:
            plot.plot_sentiment(period=period)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")

    def help_plot_sent(self):
        print('Fetches plot chart for Sentiment % change.')
        print('Usage: plot_sent -p <PERIOD>')
        print('Example: plot_sent -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
    def do_plot_nfp(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='plot nfp')
        if not args:
            print('For valid syntax, Try: plot_nfp -p 3M')
            return
        period = args.period

        print(f"Fetching plot chart for Non-Farm Payrolls: % Change from Year Ago...")
        try:
            plot.plot_nfp(period=period)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")

    def help_plot_nfp(self):
        print('Fetches plot chart for Non-Farm Payroll % change from 1-Year ago.')
        print('Usage: plot_nfp -p <PERIOD>')
        print('Example: plot_nfp -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
    def do_plot_interest(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='plot interest')
        if not args:
            print('For valid syntax, Try: plot_interest -p 3M')
            return
        period = args.period

        print(f"Fetching plot chart for Interest rates: % Change from Year Ago...")
        try:
            plot.plot_interest(period=period)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")

    def help_plot_interest(self):
        print('Fetches plot chart for Interest rates, % change from 1-Year ago.')
        print('Usage: plot_interest -p <PERIOD>')
        print('Example: plot_interest -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
    def do_plot_jobc(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='plot jobc')
        if not args:
            print('For valid syntax, Try: plot_jobc -p 3M')
            return
        period = args.period

        print(f"Fetching plot chart for Jobless Claims: % Change from Year Ago...")
        try:
            plot.plot_jobc(period=period)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")

    def help_plot_jobc(self):
        print('Fetches plot chart for Jobless Claims % change from 1-Year ago.')
        print('Usage: plot_jobc -p <PERIOD>')
        print('Example: plot_jobc -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
    def do_plot_unem(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='plot unem')
        if not args:
            print('For valid syntax, Try: plot_unem -p 3M')
            return
        period = args.period

        print(f"Fetching plot chart for Unemployment rate: % Change from Year Ago...")
        try:
            plot.plot_unemployment(period=period)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")

    def help_plot_unem(self):
        print('Fetches plot chart for Unemployment rate, % change from 1-Year ago.')
        print('Usage: plot_unem -p <PERIOD>')
        print('Example: plot_unem -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
    def do_plot_indp(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='plot indp')
        if not args:
            print('For valid syntax, Try: plot_indp -p 3M')
            return
        period = args.period

        print(f"Fetching plot chart for Industrial Production: % Change from Year Ago...")
        try:
            plot.plot_ind_prod(period=period)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")

    def help_plot_indp(self):
        print('Fetches plot chart for Industrial Production % change from 1-Year ago.')
        print('Usage: plot_indp -p <PERIOD>')
        print('Example: plot_indp -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
    def do_plot_comp(self, arg):
        def define_args(parser):
            parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
        args = parse_args(arg, define_args, prog_name='plot comp')
        if not args:
            print('For valid syntax, Try: plot_comp -p 3M')
            return
        period = args.period

        print(f"Fetching plot chart for Composite index: % Change from Year Ago...")
        try:
            plot.plot_composite(period=period)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")

    def help_plot_comp(self):
        print('Fetches plot chart for Composite index % change from 1-Year ago.')
        print('Usage: plot_comp -p <PERIOD>')
        print('Example: plot_comp -p 3M')
        print('D = Day, W = Week, M = Month, Y = Year')
#=============================================================================#
################################## CLI ########################################
#=============================================================================#
    def do_watchlist(self, arg):
        arg = arg
        print('Watchlist:')
        print(self.ticker_list)

    def help_watchlist(self):
        print('Fetches current watchlist')
        print('Usage: watchlist')
        print('Example: watchlist')
#=============================================================================#
    def do_table(self, arg):
        arg = arg
        print('Filings:')
        print(self.ticker_df.to_string(
            justify='left', 
            formatters={
                col: (lambda x: f"{x:,}" if isinstance(x, (int, float)) else x)
                for col in self.ticker_df.columns
            }
        ))

    def help_table(self):
        print('Fetches table of current filings')
        print('Usage: table')
        print('Example: table')
#=============================================================================#
############################## CLI UTILITY ####################################
#=============================================================================#
    def do_clear(self, arg):
        arg = arg
        os.system('clear')
#=============================================================================#
    def do_exit(self, arg):
        arg = arg
        print("Exiting... Goodbye!")
        return True
#=============================================================================#
if __name__ == '__main__':
    QemyShell().cmdloop()

