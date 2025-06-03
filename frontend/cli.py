from utils.env_setup import setup_wizard
setup_wizard() # First time setup + fills API_KEY variables
# Must run setup_wizard before importing backend.fetch api modules
import cmd
import os
import platform
import pandas as pd
from backend.core import plot
from backend.core.session import SessionManager
from . import parse_arg, cli_helper, cli_fred, cli_edgar, cli_tiingo
from .utils_cli import save_to_csv

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

class QemyShell(cmd.Cmd):
    intro = "Welcome to qemy. Type help or ? to list commands.\n"
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
    def do_session(self, _):
        try:
            SessionManager().run()
        except Exception as e:
            print(f"Failed to load session ERROR:\n{e}")
    def help_session(self):
        print('Starts a session.')
        print('Usage: session')
#=============================================================================#
################################### SEC #######################################
#=============================================================================#
    def do_dcf(self, arg):
        cli_edgar.dcf(arg=arg)
    def help_dcf(self):
        print('Performs DCF model evaluation on given ticker.')
        print('Usage: dcf <TICKER>')
#=============================================================================#
    def do_filing(self, arg):
        df_return = cli_edgar.filing(arg=arg, ticker_df=self.ticker_df)
        if isinstance(df_return, pd.DataFrame):
            self.ticker_df = df_return
    def help_filing(self):
        print('Fetches latest 10K/10Q metrics for given ticker.')
        print('Usage: filing <TICKER>\nFlags:')
        print('(-r --request) --- Fetches filing data directly from SEC EDGAR API.')
#=============================================================================#
    def do_bulk_refresh(self, _):
        cli_edgar.bulk_refresh()
    def help_bulk_refresh(self):
        print('Re-downloads bulk data from SEC EDGAR API with latest filings.')
        print('Note: every bulk_refresh will download and unzip ~20GB of filing data.')
        print('All previous bulk data will be overwritten.')
#=============================================================================#
################################## FRED #######################################
#=============================================================================#
    def do_rfr(self, _):
        cli_fred.rfr()
    def help_rfr(self):
        print('Fetches latest 1 year T-Bill yield.')
        print('Usage: rfr')
#=============================================================================#
    def do_cpi(self, arg):
        cli_fred.cpi(arg=arg)
    def help_cpi(self):
        print('Fetches monthly CPI data.')
        print('Usage: cpi -p <PERIOD>')
#=============================================================================#
    def do_gdp(self, arg):
        cli_fred.gdp(arg=arg)
    def help_gdp(self):
        print('Fetches quarterly GDP data.')
        print('Usage: gdp -p <PERIOD>')
#=============================================================================#
    def do_sent(self, arg):
        cli_fred.sent(arg=arg)
    def help_sent(self):
        print('Fetches cosumer sentiment data.')
        print('Usage: sent -p <PERIOD>')
#=============================================================================#
    def do_nfp(self, arg):
        cli_fred.nfp(arg=arg)
    def help_nfp(self):
        print('Fetches non-farm payroll data.')
        print('Usage: nfp -p <PERIOD>')
#=============================================================================#
    def do_interest(self, arg):
        cli_fred.interest(arg=arg)
    def help_interest(self):
        print('Fetches interest rate data.')
        print('Usage: interest -p <PERIOD>')
#=============================================================================#
    def do_jobc(self, arg):
        cli_fred.jobc(arg=arg)
    def help_jobc(self):
        print('Fetches jobless claim data.')
        print('Usage: jobc -p <PERIOD>')
#=============================================================================#
    def do_unem(self, arg):
        cli_fred.unem(arg=arg)
    def help_unem(self):
        print('Fetches unemployment data.')
        print('Usage: unem -p <PERIOD>')
#=============================================================================#
    def do_indp(self, arg):
        cli_fred.indp(arg=arg)
    def help_indp(self):
        print('Fetches industrial production data.')
        print('Usage: indp -p <PERIOD>')
#=============================================================================#
    def do_netex(self, arg):
        cli_fred.netex(arg=arg)
    def help_netex(self):
        print('Fetches real net exports of goods and services data.')
        print('Usage: netex -p <PERIOD>')
#=============================================================================#
################################## PRICE ######################################
#=============================================================================#
    def do_price(self, arg):
        cli_tiingo.price(arg=arg)
    def help_price(self):
        print('Fetches daily closing prices for given ticker.')
        print('Usage: price <TICKER> -p <PERIOD>')
#=============================================================================#
################################## PLOT #######################################
#=============================================================================#
    def do_plot_price(self, arg):
        period, ticker = parse_arg.parse_arg_p_t(arg=arg, name='plot_price')
        if isinstance(period, str) and isinstance(ticker, str):
            print(f"Fetching plot chart for: {ticker} daily closing prices, log scaled...")
            try:
                plot.plot_price(ticker=ticker, period=period)
            except Exception as e:
                print(f"Could not fetch plot chart, please try another ticker. Error:\n{e}")
        else:
            print('For valid syntax, Try: plot_price AAPL -p 3M')
    def help_plot_price(self):
        print('Fetches plot chart of log scaled daily prices for given ticker.')
        print('Usage: plot_price <TICKER> -p <PERIOD>')
#=============================================================================#
    def do_plot_lr(self, arg):
        period, ticker = parse_arg.parse_arg_p_t(arg=arg, name='plot_lr')
        if isinstance(period, str) and isinstance(ticker, str):
            print(f"Fetching plot chart for: {ticker} daily closing prices...")
            try:
                plot.plot_lr(ticker=ticker, period=period)
            except Exception as e:
                print(f"Could not fetch plot chart, please try another ticker. Error:\n{e}")
        else:
            print('For valid syntax, Try: price_plot AAPL -p 3M')
    def help_plot_lr(self):
        print('Fetches linear regression beta comparison for given ticker.')
        print('Usage: plot_lr <TICKER> -p <PERIOD>')
#=============================================================================#
    def do_plot_cpi(self, arg):
        period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_cpi')
        units = 'pc1' if units is None else units
        if isinstance(period, str) and isinstance(save_state, str):
            print(f"Fetching plot chart for CPI inflation: % Change from Year Ago...")
            try:
                if save_state in ('Y', 'YES'):
                    plot.plot_cpi(period=period, save=True, units=units)
                else:
                    plot.plot_cpi(period=period, save=False, units=units)
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_cpi -p 3m -s yes')
    def help_plot_cpi(self):
        print('Fetches plot chart for CPI inflation % change from 1-Year ago.')
        print('Usage: plot_cpi -p <PERIOD>')
#=============================================================================#
    def do_plot_gdp(self, arg):
        period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_gdp')
        units = 'pc1' if units is None else units
        if isinstance(period, str) and isinstance(save_state, str):
            print(f"Fetching plot chart for GDP: % Change from Year Ago...")
            try:
                if save_state in ('Y', 'YES'):
                    plot.plot_gdp(period=period, save=True, units=units)
                else:
                    plot.plot_gdp(period=period, save=False, units=units)
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_gdp -p 3M -s yes')
    def help_plot_gdp(self):
        print('Fetches plot chart for GDP % change from 1-Year ago.')
        print('Usage: plot_gdp -p <PERIOD>')
#=============================================================================#
    def do_plot_sent(self, arg):
        period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_sent')
        units = 'pch' if units is None else units
        if isinstance(period, str) and isinstance(save_state, str):
            print(f"Fetching plot chart for Sentiment: % Change...")
            try:
                if save_state in ('Y', 'YES'):
                    plot.plot_sentiment(period=period, save=True, units=units)
                else:
                    plot.plot_sentiment(period=period, save=False, units=units)
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_sent -p 3M -s yes')
    def help_plot_sent(self):
        print('Fetches plot chart for Sentiment % change.')
        print('Usage: plot_sent -p <PERIOD>')
#=============================================================================#
    def do_plot_nfp(self, arg):
        period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_nfp')
        units = 'pc1' if units is None else units
        if isinstance(period, str) and isinstance(save_state, str):
            print(f"Fetching plot chart for Non-Farm Payrolls: % Change from Year Ago...")
            try:
                if save_state in ('Y', 'YES'):
                    plot.plot_nfp(period=period, save=True, units=units)
                else:
                    plot.plot_nfp(period=period, save=False, units=units)
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_nfp -p 3M -s yes')
    def help_plot_nfp(self):
        print('Fetches plot chart for Non-Farm Payroll % change from 1-Year ago.')
        print('Usage: plot_nfp -p <PERIOD>')
#=============================================================================#
    def do_plot_interest(self, arg):
        period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_interest')
        units = 'pc1' if units is None else units
        if isinstance(period, str) and isinstance(save_state, str):
            print(f"Fetching plot chart for Interest rates: % Change from Year Ago...")
            try:
                if save_state in ('Y', 'YES'):
                    plot.plot_interest(period=period, save=True, units=units)
                else:
                    plot.plot_interest(period=period, save=False, units=units)
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_interest -p 3M -s yes')
    def help_plot_interest(self):
        print('Fetches plot chart for Interest rates, % change from 1-Year ago.')
        print('Usage: plot_interest -p <PERIOD>')
#=============================================================================#
    def do_plot_jobc(self, arg):
        period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_jobc')
        units = 'pc1' if units is None else units
        if isinstance(period, str) and isinstance(save_state, str):
            print(f"Fetching plot chart for Jobless Claims: % Change from Year Ago...")
            try:
                if save_state in ('Y', 'YES'):
                    plot.plot_jobc(period=period, save=True, units=units)
                else:
                    plot.plot_jobc(period=period, save=False, units=units)
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_jobc -p 3M -s yes')
    def help_plot_jobc(self):
        print('Fetches plot chart for Jobless Claims % change from 1-Year ago.')
        print('Usage: plot_jobc -p <PERIOD>')
#=============================================================================#
    def do_plot_unem(self, arg):
        period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_unem')
        units = 'pc1' if units is None else units
        if isinstance(period, str) and isinstance(save_state, str):
            print(f"Fetching plot chart for Unemployment rate: % Change from Year Ago...")
            try:
                if save_state in ('Y', 'YES'):
                    plot.plot_unemployment(period=period, save=True, units=units)
                else:
                    plot.plot_unemployment(period=period, save=False, units=units)
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_unem -p 3M -s yes')
    def help_plot_unem(self):
        print('Fetches plot chart for Unemployment rate, % change from 1-Year ago.')
        print('Usage: plot_unem -p <PERIOD>')
#=============================================================================#
    def do_plot_indp(self, arg):
        period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_indp')
        units = 'pc1' if units is None else units
        if isinstance(period, str) and isinstance(save_state, str):
            print(f"Fetching plot chart for Industrial Production: % Change from Year Ago...")
            try:
                if save_state in ('Y', 'YES'):
                    plot.plot_ind_prod(period=period, save=True, units=units)
                else:
                    plot.plot_ind_prod(period=period, save=False, units=units)
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_indp -p 3M -s yes')
    def help_plot_indp(self):
        print('Fetches plot chart for Industrial Production % change from 1-Year ago.')
        print('Usage: plot_indp -p <PERIOD>')
#=============================================================================#
    def do_plot_netex(self, arg):
        period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_netex')
        units = 'lin' if units is None else units
        if isinstance(period, str) and isinstance(save_state, str):
            print(f"Fetching plot chart for Real Net Exports of Goods and Services...")
            try:
                if save_state in ('Y', 'YES'):
                    plot.plot_netex(period=period, save=True, units=units)
                else:
                    plot.plot_netex(period=period, save=False, units=units)
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_netex -p 3M -s yes')
    def help_plot_netex(self):
        print('Fetches plot chart for Real Net Exports of Goods and Services.')
        print('Usage: plot_netex -p <PERIOD>')
#=============================================================================#
################################## CLI ########################################
#=============================================================================#
    def do_watchlist(self, _):
        print('Watchlist:')
        print(self.ticker_list)
    def help_watchlist(self):
        print('Fetches current watchlist')
        print('Usage: watchlist')
#=============================================================================#
    def do_table(self, arg):
        save_state = parse_arg.parse_arg_s(arg=arg, name='table')
        if isinstance(save_state, str):
            try:
                if save_state in ('Y', 'YES'):
                    save_to_csv(df=self.ticker_df)
                    print('File saved...\n /qemy/exports/tables/')
                else:
                    print('Filings:')
                    print(self.ticker_df.to_string(justify='left', formatters={
                        col: (lambda x: f"{x:,}" if isinstance(x, (int, float)) else x)
                        for col in self.ticker_df.columns
                    }))
            except Exception as e:
                print(f"Could not fetch/save table. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: table -s yes')
    def help_table(self):
        print('Fetches table of current filings')
        print('Usage: table')
#=============================================================================#
################################ CLI UTIL #####################################
#=============================================================================#
    def do_calc(self, arg):
        try:
            result = eval(arg, {"__builtins__": {}}, {})
            print(result)
        except:
            print("Invalid expression")
    def help_calc(self):
        print("Simple calculator with Python syntax")
        print("Example: calc 2 + 2")
#=============================================================================#
    def do_help(self, arg):
        if arg:
            super().do_help(arg)
        else:
            cli_helper.help()
#=============================================================================#
    def do_clear(self, _):
        clear_screen = 'cls' if platform.system() == 'Windows' else 'clear'
        os.system(clear_screen)
#=============================================================================#
    def do_exit(self, _):
        print("Exiting... Goodbye!")
        return True
#=============================================================================#
if __name__ == '__main__':
    QemyShell().cmdloop()

