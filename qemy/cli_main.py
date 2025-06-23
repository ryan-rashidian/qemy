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
    intro = "Qemy v0.1.0\nType \"help\" or \"?\" for more information.\n"
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

    def do_plot(self, arg):
        cli_plot.PlotCmd(arg=arg).run()

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

