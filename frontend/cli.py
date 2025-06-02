from utils.env_setup import setup_wizard
setup_wizard() # First time setup + fills API_KEY variables
# Must run setup_wizard before importing backend.fetch api modules
import cmd
import os
import pandas as pd
from backend.core import plot
from backend.core.dcf import get_dcf_eval
from backend.core.session import SessionManager
from backend.fetch import api_tiingo as tiingo
from backend.fetch import api_fred as fred
from backend.fetch.api_edgar import SEC_Filings
from backend.fetch.api_edgar_bulk import bulk_refresh
from . import parse_arg 
from .utils_cli import save_to_csv

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
#=============================================================================#
################################### SEC #######################################
#=============================================================================#
    def do_filing(self, arg):
        if ' -r' in arg:
            ticker = arg.replace('-r', '').strip().upper() 
            use_requests = True
        if ' --request' in arg:
            ticker = arg.replace('--request', '').strip().upper() 
            use_requests = True
        else:
            ticker = arg.strip().upper()
            use_requests = False
        print(f"Fetching latest 10K/10Q filing metrics for {ticker}")
        try:
            df = SEC_Filings(ticker=ticker, use_requests=use_requests).get_metrics() 
            if isinstance(df, pd.DataFrame): 
                self.ticker_df[ticker] = df[ticker]
                print(df.to_string(justify='left', formatters={
                    ticker: lambda x: f"{x:,}" if isinstance(x, (int, float)) else x
                }))
        except:
            print('Could not fetch filing metrics, please try another ticker.')
    def help_filing(self):
        print('Fetches latest 10K/10Q metrics for given ticker.')
        print('Usage: filing <TICKER>\nFlags:')
        print('(-r --request) --- Fetches filing data directly from SEC EDGAR API.')
#=============================================================================#
    def do_dcf(self, arg):
        get_dcf_eval(arg)
    def help_dcf(self):
        print('Performs DCF model evaluation on given ticker.')
        print('Usage: dcf <TICKER>')
#=============================================================================#
    def do_bulk_refresh(self, arg):
        arg = arg
        confirm = input("All previous bulk data will be overwritten.\nAre you sure? (yes/no): ")
        if confirm.strip().lower() == 'yes':
            try:
                bulk_refresh()
            except Exception as e:
                print(f"Bulk refresh failed. Error:\n{e}")
    def help_bulk_refresh(self):
        print('Re-downloads bulk data from SEC EDGAR API with latest filings.')
        print('Note: every bulk_refresh will download and unzip ~20GB of filing data.')
        print('All previous bulk data will be overwritten.')
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
#=============================================================================#
    def do_cpi(self, arg):
        period, units = parse_arg.parse_arg_p_u(arg=arg, name='cpi')
        units = 'pc1' if units is None else units
        if isinstance(period, str):
            try:
                print(fred.get_cpi_inflation(period=period, units=units))
            except Exception as e:
                print(f"Could not fetch data ERROR:\n{e}")
        else:
            print('For valid syntax, Try: cpi -p 1Y')
    def help_cpi(self):
        print('Fetches monthly CPI data.')
        print('Usage: cpi -p <PERIOD>')
#=============================================================================#
    def do_gdp(self, arg):
        period, units = parse_arg.parse_arg_p_u(arg=arg, name='gdp')
        units = 'pc1' if units is None else units
        if isinstance(period, str):
            try:
                print(fred.get_gdp(period=period, units=units))
            except Exception as e:
                print(f"Could not fetch data ERROR:\n{e}")
        else:
            print('For valid syntax, Try: gdp -p 1Y')
    def help_gdp(self):
        print('Fetches quarterly GDP data.')
        print('Usage: gdp -p <PERIOD>')
#=============================================================================#
    def do_sent(self, arg):
        period, units = parse_arg.parse_arg_p_u(arg=arg, name='sent')
        units = 'pch' if units is None else units
        if isinstance(period, str):
            try:
                print(fred.get_sentiment(period=period, units=units))
            except Exception as e:
                print(f"Could not fetch data ERROR:\n{e}")
        else:
            print('For valid syntax, Try: sent -p 1Y')
    def help_sent(self):
        print('Fetches cosumer sentiment data.')
        print('Usage: sent -p <PERIOD>')
#=============================================================================#
    def do_nfp(self, arg):
        period, units = parse_arg.parse_arg_p_u(arg=arg, name='nfp')
        units = 'pc1' if units is None else units
        if isinstance(period, str):
            try:
                print(fred.get_nf_payrolls(period=period, units=units))
            except Exception as e:
                print(f"Could not fetch data ERROR:\n{e}")
        else:
            print('For valid syntax, Try: nfp -p 1Y')
    def help_nfp(self):
        print('Fetches non-farm payroll data.')
        print('Usage: nfp -p <PERIOD>')
#=============================================================================#
    def do_interest(self, arg):
        period, units = parse_arg.parse_arg_p_u(arg=arg, name='interest')
        units = 'pc1' if units is None else units
        if isinstance(period, str):
            try:
                print(fred.get_interest(period=period, units=units))
            except Exception as e:
                print(f"Could not fetch data ERROR:\n{e}")
        else:
            print('For valid syntax, Try: interest -p 1Y')
    def help_interest(self):
        print('Fetches interest rate data.')
        print('Usage: interest -p <PERIOD>')
#=============================================================================#
    def do_jobc(self, arg):
        period, units = parse_arg.parse_arg_p_u(arg=arg, name='jobc')
        units = 'pc1' if units is None else units
        if isinstance(period, str):
            try:
                print(fred.get_jobless_claims(period=period, units=units))
            except Exception as e:
                print(f"Could not fetch data ERROR:\n{e}")
        else:
            print('For valid syntax, Try: jobc -p 1Y')
    def help_jobc(self):
        print('Fetches jobless claim data.')
        print('Usage: jobc -p <PERIOD>')
#=============================================================================#
    def do_unem(self, arg):
        period, units = parse_arg.parse_arg_p_u(arg=arg, name='unem')
        units = 'pc1' if units is None else units
        if isinstance(period, str):
            try:
                print(fred.get_unemployment(period=period, units=units))
            except Exception as e:
                print(f"Could not fetch data ERROR:\n{e}")
        else:
            print('For valid syntax, Try: unem -p 1Y')
    def help_unem(self):
        print('Fetches unemployment data.')
        print('Usage: unem -p <PERIOD>')
#=============================================================================#
    def do_indp(self, arg):
        period, units = parse_arg.parse_arg_p_u(arg=arg, name='indp')
        units = 'pc1' if units is None else units
        if isinstance(period, str):
            try:
                print(fred.get_ind_prod(period=period, units=units))
            except Exception as e:
                print(f"Could not fetch data ERROR:\n{e}")
        else:
            print('For valid syntax, Try: indp -p 1Y')
    def help_indp(self):
        print('Fetches industrial production data.')
        print('Usage: indp -p <PERIOD>')
#=============================================================================#
    def do_netex(self, arg):
        period, units = parse_arg.parse_arg_p_u(arg=arg, name='netex')
        units = 'lin' if units is None else units 
        if isinstance(period, str) and isinstance(units, str):
            try:
                print(fred.get_netex(period=period, units=units.lower()))
            except Exception as e:
                print(f"Could not fetch data ERROR:\n{e}")
        else:
            print('For valid syntax, Try: netex -p 1Y')
    def help_netex(self):
        print('Fetches real net exports of goods and services data.')
        print('Usage: netex -p <PERIOD>')
#=============================================================================#
################################## PRICE ######################################
#=============================================================================#
    def do_price(self, arg):
        period, ticker = parse_arg.parse_arg_p_t(arg=arg, name='price')
        if isinstance(period, str) and isinstance(ticker, str):
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
        else:
            print('For valid syntax, Try: price AAPL -p 3M')
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
    def do_watchlist(self, arg):
        arg = arg
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

