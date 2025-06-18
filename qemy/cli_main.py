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

#================================== CORE =====================================#

    def do_table(self, arg):
        cli_core.table(arg=arg, ticker_df=self.ticker_df)

    def do_wl(self, arg):
        ticker_list = cli_core.watch_list(arg=arg, ticker_list=self.ticker_list.copy())
        if ticker_list:
            self.ticker_list = ticker_list
        else:
            return

#================================== EDGAR ====================================#

    def do_f(self, arg):
        df_return = cli_edgar.filing(arg=arg, ticker_df=self.ticker_df)
        if isinstance(df_return, pd.DataFrame):
            self.ticker_df = df_return

    def do_fmetric(self, arg):
        cli_edgar.filing_metric(arg=arg)

#================================== FRED =====================================#

    def do_fred(self, arg):
        cli_fred.FREDCmd(arg=arg).run()

#================================== TIINGO ===================================#

    def do_quote(self, arg):
        cli_tiingo.quote(arg=arg)

    def do_price(self, arg):
        cli_tiingo.price(arg=arg)

#================================== PLOT =====================================#

    def do_plot_price(self, arg):
        cli_plot.plot_price(arg=arg)
    def help_plot_price(self):
        print("Fetches plot chart of log scaled daily prices for given ticker.")
        print("Usage: plot_price <TICKER> -p <PERIOD>")

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
            super().do_help(arg) # temporary until full -h refactor
        else:
            cli_helper.help()

    def do_econ(self, _):
        cli_helper.econ()

    def do_market(self, _):
        cli_helper.market()

    def do_plugins(self, _):
        cli_helper.plugins()

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

    def do_bulk_refresh(self, arg):
        cli_aux.bulk_refresh(arg=arg)

    def do_calc(self, arg):
        cli_aux.calc(arg=arg)

    def do_env_reset(self, arg):
        cli_aux.env_reset(arg=arg)

#=============================================================================#

def main():
    QemyShell().cmdloop()

if __name__ == '__main__':
    main()

