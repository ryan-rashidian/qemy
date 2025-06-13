from qemy.utils.env_setup import setup_wizard
setup_wizard() # First time setup + fills API_KEY variables
# Must run setup_wizard before importing qemy modules
import cmd
import os
import platform
import pandas as pd
from qemy.cli import cli_helper, cli_fred, cli_edgar, cli_tiingo, cli_plot, cli_aux, cli_core, cli_plugins

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#=============================================================================#

class QemyShell(cmd.Cmd):
    intro = "Welcome to qemy. Type help or ? to list commands.\n"
    prompt = "qemy> "
    def __init__(self):
        metric_index = pd.Index([
            'Form', 'Filed', 'Shares Outstanding', 'Cash & Equivalents', 'Total Debt',
            'Net Debt', 'Revenue', 'COGS', 'Gross Profit', 'EBIT', 'Net Income', 'Assets', 
            'Liabilities', 'Equity', 'OpEx', 'CapEx', 'OCF', 'FCF', 'EPS', 
        ])
        super().__init__()
        self.ticker_list = []
        self.ticker_df = pd.DataFrame(index=metric_index) 
        self.ticker_df.index.name = 'Metrics:'

#================================== PLUGINS ==================================#

    def do_m(self, arg):
        cli_plugins.run_models(arg=arg)
    def help_m(self):
        print("Runs a given plugin model")
        print("Usage: m <MODEL>")

#================================== CORE =====================================#

    def do_table(self, arg):
        cli_core.table(arg=arg, ticker_df=self.ticker_df)
    def help_table(self):
        print("Fetches table of current filings")
        print("Usage: table")

    def do_wl(self, _):
        try:
            ticker_list = cli_core.WatchListManager(ticker_list=self.ticker_list.copy()).run()
            if ticker_list:
                self.ticker_list = ticker_list
            else:
                return
        except Exception as e:
            print(f"Failed to load watchlist, Error:\n{e}")
    def help_wl(self):
        print("Starts watchlist editor.")
        print("Usage: watchlist")

#================================== EDGAR ====================================#

    def do_f(self, arg):
        df_return = cli_edgar.filing(arg=arg, ticker_df=self.ticker_df)
        if isinstance(df_return, pd.DataFrame):
            self.ticker_df = df_return
    def help_f(self):
        print("Fetches latest 10K/10Q/20F metrics for given ticker.")
        print("Usage: filing <TICKER>\nFlags:")
        print("(-r --request) --- Fetches filing data directly from SEC EDGAR API.")

    def do_fmetric(self, arg):
        cli_edgar.filing_metric(arg=arg)
    def help_fmetric(self):
        print("Fetches --metric history from 10K/10Q/20F filings for given ticker.")
        print("Usage: fmetric <TICKER> -m <METRIC> -q <#_Of_Quarters>")

#================================== FRED =====================================#

    def do_rfr(self, _):
        cli_fred.rfr()
    def help_rfr(self):
        print("Fetches latest 1 year T-Bill yield.")
        print("Usage: rfr")

    def do_cpi(self, arg):
        cli_fred.cpi(arg=arg)
    def help_cpi(self):
        print("Fetches monthly CPI data.")
        print("Usage: cpi -p <PERIOD>")

    def do_gdp(self, arg):
        cli_fred.gdp(arg=arg)
    def help_gdp(self):
        print("Fetches quarterly GDP data.")
        print("Usage: gdp -p <PERIOD>")

    def do_sent(self, arg):
        cli_fred.sent(arg=arg)
    def help_sent(self):
        print("Fetches Cosumer Sentiment index data.")
        print("Usage: sent -p <PERIOD>")

    def do_nfp(self, arg):
        cli_fred.nfp(arg=arg)
    def help_nfp(self):
        print("Fetches Nonfarm Payroll data.")
        print("Usage: nfp -p <PERIOD>")

    def do_interest(self, arg):
        cli_fred.interest(arg=arg)
    def help_interest(self):
        print("Fetches Interest RED rate data.")
        print("Usage: Interest -p <PERIOD>")

    def do_jobc(self, arg):
        cli_fred.jobc(arg=arg)
    def help_jobc(self):
        print("Fetches Jobless Claim data.")
        print("Usage: jobc -p <PERIOD>")

    def do_unem(self, arg):
        cli_fred.unem(arg=arg)
    def help_unem(self):
        print("Fetches Unemployment data.")
        print("Usage: unem -p <PERIOD>")

    def do_indp(self, arg):
        cli_fred.indp(arg=arg)
    def help_indp(self):
        print("Fetches Industrial Production data.")
        print("Usage: indp -p <PERIOD>")

    def do_netex(self, arg):
        cli_fred.netex(arg=arg)
    def help_netex(self):
        print("Fetches Real Net Exports of Goods and Services data.")
        print("Usage: netex -p <PERIOD>")

#================================== TIINGO ===================================#

    def do_quote(self, arg):
        cli_tiingo.quote(arg=arg)
    def help_quote(self):
        print("Fetches latest price quote for given ticker.")
        print("Usage: quote <TICKER>")

    def do_price(self, arg):
        cli_tiingo.price(arg=arg)
    def help_price(self):
        print("Fetches daily closing prices for given ticker.")
        print("Usage: price <TICKER> -p <PERIOD>")

#================================== MODEL ====================================#
    
    def do_dcf(self, arg):
        cli_model.dcf(arg=arg)
    def help_dcf(self):
        print("Performs DCF model evaluation on given ticker.")
        print("Usage: dcf <TICKER>")

    def do_lr(self, arg):
        cli_model.lr(arg=arg)
    def help_lr(self):
        print("Fetches daily closing prices for given ticker and performs linear calculation.")
        print("Usage: lr <TICKER> -p <PERIOD>")
        print("Uses SPY ETF Trust as dependent variable.")

    def do_mcarlo(self, arg):
        cli_model.monte_carlo(arg=arg)
    def help_mcarlo(self):
        print("Performs Monte Carlo simulations on given ticker's price history")
        print("Usage: mcarlo AAPL -p 2Y -n 1000")

#================================== PLOT =====================================#

    def do_plot_price(self, arg):
        cli_plot.plot_price(arg=arg)
    def help_plot_price(self):
        print("Fetches plot chart of log scaled daily prices for given ticker.")
        print("Usage: plot_price <TICKER> -p <PERIOD>")

    def do_plot_lr(self, arg):
        cli_plot.plot_lr(arg=arg)
    def help_plot_lr(self):
        print("Fetches linear regression plot chart for given ticker and SPY.")
        print("Usage: plot_lr <TICKER> -p <PERIOD>")

    def do_plot_mcarlo(self, arg):
        cli_plot.plot_monte_carlo(arg=arg)
    def help_plot_mcarlo(self):
        print("Performs and plots Monte Carlo simulations on given ticker's price history")
        print("Usage: plot_mcarlo AAPL -p 2Y -n 1000")

    def do_plot_cpi(self, arg):
        cli_plot.plot_cpi(arg=arg)
    def help_plot_cpi(self):
        print("Fetches plot chart for CPI inflation.")
        print("Usage: plot_cpi -p <PERIOD>")

    def do_plot_gdp(self, arg):
        cli_plot.plot_gdp(arg=arg)
    def help_plot_gdp(self):
        print("Fetches plot chart for GDP.")
        print("Usage: plot_gdp -p <PERIOD>")

    def do_plot_sent(self, arg):
        cli_plot.plot_sent(arg=arg)
    def help_plot_sent(self):
        print("Fetches plot chart for Sentiment index.")
        print("Usage: plot_sent -p <PERIOD>")

    def do_plot_nfp(self, arg):
        cli_plot.plot_nfp(arg=arg)
    def help_plot_nfp(self):
        print("Fetches plot chart for Non-Farm Payroll.")
        print("Usage: plot_nfp -p <PERIOD>")

    def do_plot_interest(self, arg):
        cli_plot.plot_interest(arg=arg)
    def help_plot_interest(self):
        print("Fetches plot chart for Interest FED rate.")
        print("Usage: plot_interest -p <PERIOD>")

    def do_plot_jobc(self, arg):
        cli_plot.plot_jobc(arg=arg)
    def help_plot_jobc(self):
        print("Fetches plot chart for Jobless Claims.")
        print("Usage: plot_jobc -p <PERIOD>")

    def do_plot_unem(self, arg):
        cli_plot.plot_unem(arg=arg)
    def help_plot_unem(self):
        print("Fetches plot chart for Unemployment rate.")
        print("Usage: plot_unem -p <PERIOD>")

    def do_plot_indp(self, arg):
        cli_plot.plot_indp(arg=arg)
    def help_plot_indp(self):
        print("Fetches plot chart for Industrial Production.")
        print("Usage: plot_indp -p <PERIOD>")

    def do_plot_netex(self, arg):
        cli_plot.plot_netex(arg=arg)
    def help_plot_netex(self):
        print("Fetches plot chart for Real Net Exports of Goods and Services.")
        print("Usage: plot_netex -p <PERIOD>")

#================================== HELPER ===================================#

    def do_help(self, arg):
        if arg:
            super().do_help(arg)
        else:
            cli_helper.help()

    def do_econ(self, _):
        cli_helper.econ()

    def do_market(self, _):
        cli_helper.market()

    def do_models(self, _):
        cli_helper.model()

    def do_plots(self, _):
        cli_helper.plot()

    def do_flags(self, _):
        cli_helper.flags()

    def do_units(self, _):
        cli_helper.units()

    def do_metrics(self, _):
        cli_helper.metrics()

#================================== AUX ======================================#

    def do_clear(self, _):
        clear_screen = 'cls' if platform.system() == 'Windows' else 'clear'
        os.system(clear_screen)
    def do_cls(self, _):
        clear_screen = 'cls' if platform.system() == 'Windows' else 'clear'
        os.system(clear_screen)

    def do_exit(self, _):
        print("Exiting... Goodbye!")
        return True
    def do_q(self, _):
        print("Exiting... Goodbye!")
        return True

    def do_bulk_refresh(self, _):
        cli_aux.bulk_refresh()
    def help_bulk_refresh(self):
        print("Re-downloads bulk data from SEC EDGAR API with latest filings.")
        print("Note: every bulk_refresh will download and unzip ~20GB of filing data.")
        print("All previous bulk data will be overwritten.")

    def do_calc(self, arg):
        try:
            result = eval(arg, {"__builtins__": {}}, {})
            print(result)
        except:
            print("Invalid expression")
    def help_calc(self):
        print("Simple calculator with Python syntax")
        print("Example: calc 2 + 2")

    def do_env_reset(self, _):
        cli_aux.env_reset()
    def help_env_reset(self):
        print("Deletes the .env files containing your current API keys and User Agent information.")
        print("This command will also exit qemy, and users will have to complete the setup wizard again.")

#=============================================================================#

def main():
    QemyShell().cmdloop()

if __name__ == '__main__':
    main()

