import cmd
import os
import platform

import pandas as pd

from qemy.utils.env_setup import setup_wizard

from .apis import cli_edgar, cli_fred, cli_tiingo
from .core import aux, cli_metrics, cli_plots, cli_plugins, core, helper

setup_wizard()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#=============================================================================#

class QemyShell(cmd.Cmd):
    intro = "Qemy CLI 0.1.1\nType \"help\" or \"?\" for more information.\n"
    prompt = "qemy> "

    def __init__(self):
        super().__init__()
        self.debug_mode = False
        self.ticker_list = []
        self.ticker_df = pd.DataFrame()

# === PLUGINS ===
    def do_m(self, arg):
        cli_plugins.run_models(arg=arg)

# === CORE ===
    def do_table(self, arg):
        core.table(arg=arg, ticker_df=self.ticker_df)

    def do_wl(self, arg):
        ticker_list = core.watch_list(
            arg=arg,
            ticker_list=self.ticker_list.copy()
        )
        if ticker_list:
            self.ticker_list = ticker_list
        else:
            return

# === EDGAR ===
    def do_f(self, arg):
        df_return = cli_edgar.filing(
            arg=arg,
            ticker_df=self.ticker_df.copy()
        )
        if isinstance(df_return, pd.DataFrame):
            self.ticker_df = df_return

# === FRED ===
    def do_fred(self, arg):
        cli_fred.FREDCmd(arg=arg).run()

# === TIINGO ===
    def do_quote(self, arg):
        cli_tiingo.quote(arg=arg)

    def do_price(self, arg):
        cli_tiingo.price(arg=arg)

# === PLOT ===
    def do_plot(self, arg):
        cli_plots.PlotCmd(arg=arg).run()

# === METRIC ===
    def do_metric(self, arg):
        cli_metrics.MetricCmd(arg=arg).run()

# === HELPER ===
    def do_help(self, arg):
        if arg:
            print(f"'{arg}' Use '<COMMAND> -h' for help menu")
        else:
            helper.help()

    def do_econ(self, _):
        helper.econ()

    def do_market(self, _):
        helper.market()

    def do_plugins(self, _):
        helper.plugins()

    def do_flags(self, _):
        helper.flags()

    def do_units(self, _):
        helper.units()

    def do_metrics(self, _):
        helper.metrics()

# === AUX ===
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
        aux.bulk_refresh(arg=arg)

    def do_calc(self, arg):
        aux.calc(arg=arg)

    def do_debug(self, arg):
        toggle = aux.debug(arg=arg, debug_mode=self.debug_mode)
        if toggle is not None:
            self.debug_mode = toggle

    def do_env_reset(self, arg):
        aux.env_reset(arg=arg)

#=============================================================================#

