from qemy.core.plot import plot
from qemy.core.plot.plot_fred import PlotFRED

from .._parse_args import check_help, parse_args_cli
from .helper import print_help_table

# === PLOT ===

class PlotCmd:
    def __init__(self, arg):
        self.help_requested = False
        self.failed = False

        if check_help(
            arg_str=arg,
            help_func=lambda: print_help_table(" plot ", [
                ("Available Commands:", ""),
                ("price", ""),
                ("cpi", ""),
                ("gdp", ""),
                ("sent", ""),
                ("nfp", ""),
                ("interest", ""),
                ("jobc", ""),
                ("unem", ""),
                ("indp", ""),
                ("netex", ""),
                ("Usage:", "plot <COMMAND>\n"),
            ])
        ):
            self.help_requested = True
            return


        core_args, plugin_kwargs, other_args = parse_args_cli(
            arg_str=arg,
            expected_args=[
                'period', 'ticker_flag', 'save',
                'units', 'plot_p', 'help'
            ],
            prog_name='FREDCmd',
        )

        if plugin_kwargs or other_args:
            print(f"Unexpected command: {other_args} {plugin_kwargs}")
            self.failed = True
            return

        (
            self.period,
            self.ticker,
            self.save_state,
            self.units,
            self.plot,
            self.help
        ) = core_args

    def price(self):
        if isinstance(self.period, str) and isinstance(self.ticker, str):
            print(f"Fetching plot chart for: {self.ticker}, log scaled...")
            try:
                plot.plot_price(ticker=self.ticker, period=self.period)
            except Exception as e:
                print(f"Failed to fetch plot chart.\n{e}")
        else:
            print('For valid syntax, Try: plot price AAPL -p 3M')

    def cpi(self):
        if not self.save_state:
            self.save_state = False
        self.units = 'pc1' if self.units is None else self.units

        if isinstance(self.period, str):
            print("Plotting Consumer Price Index...")
            try:
                PlotFRED().plot_cpi(
                    period=self.period,
                    save=self.save_state,
                    units=self.units
                )
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot cpi -p 3m -s yes')

    def gdp(self):
        if not self.save_state:
            self.save_state = False
        self.units = 'pc1' if self.units is None else self.units

        if isinstance(self.period, str):
            print("Plotting Gross Domestic Product...")
            try:
                PlotFRED().plot_gdp(
                    period=self.period,
                    save=self.save_state,
                    units=self.units
                )
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot gdp -p 3M -s yes')

    def sent(self):
        if not self.save_state:
            self.save_state = False
        self.units = 'pch' if self.units is None else self.units

        if isinstance(self.period, str):
            print("Plotting Consumer Sentiment Index...")
            try:
                PlotFRED().plot_sentiment(
                    period=self.period,
                    save=self.save_state,
                    units=self.units
                )
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_sent -p 3M -s yes')

    def nfp(self):
        if not self.save_state:
            self.save_state = False
        self.units = 'pc1' if self.units is None else self.units

        if isinstance(self.period, str):
            print("Plotting Non-Farm Payrolls...")
            try:
                PlotFRED().plot_nfp(
                    period=self.period,
                    save=self.save_state,
                    units=self.units
                )
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_nfp -p 3M -s yes')

    def interest(self):
        if not self.save_state:
            self.save_state = False
        self.units = 'pc1' if self.units is None else self.units

        if isinstance(self.period, str):
            print("Plotting Interest Rates...")
            try:
                PlotFRED().plot_interest(
                    period=self.period,
                    save=self.save_state,
                    units=self.units
                )
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_interest -p 3M -s yes')

    def jobc(self):
        if not self.save_state:
            self.save_state = False
        self.units = 'pc1' if self.units is None else self.units

        if isinstance(self.period, str):
            print("Plotting Jobless Claims...")
            try:
                PlotFRED().plot_jobc(
                    period=self.period,
                    save=self.save_state,
                    units=self.units
                )
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_jobc -p 3M -s yes')

    def unem(self):
        if not self.save_state:
            self.save_state = False
        self.units = 'pc1' if self.units is None else self.units

        if isinstance(self.period, str):
            print("Plotting Unemployment Rate...")
            try:
                PlotFRED().plot_unem(
                    period=self.period,
                    save=self.save_state,
                    units=self.units
                )
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_unem -p 3M -s yes')

    def indp(self):
        if not self.save_state:
            self.save_state = False
        self.units = 'pc1' if self.units is None else self.units

        if isinstance(self.period, str):
            print("Plotting Industrial Production...")
            try:
                PlotFRED().plot_indp(
                    period=self.period,
                    save=self.save_state,
                    units=self.units
                )
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_indp -p 3M -s yes')

    def netex(self):
        if not self.save_state:
            self.save_state = False
        self.units = 'lin' if self.units is None else self.units

        if isinstance(self.period, str):
            print("Plotting Real Net Exports of Goods and Services...")
            try:
                PlotFRED().plot_netex(
                    period=self.period,
                    save=self.save_state,
                    units=self.units
                )
            except Exception as e:
                print(f"Could not fetch plot chart. ERROR:\n{e}")
        else:
            print('For valid syntax, Try: plot_netex -p 3M -s yes')

    def run(self):
        if self.help_requested or self.failed:
            return
        elif self.plot == 'PRICE':
            self.price()
        elif self.plot == 'CPI':
            self.cpi()
        elif self.plot == 'GDP':
            self.gdp()
        elif self.plot == 'SENT':
            self.sent()
        elif self.plot == 'NFP':
            self.nfp()
        elif self.plot == 'INTEREST':
            self.interest()
        elif self.plot == 'JOBC':
            self.jobc()
        elif self.plot == 'UNEM':
            self.unem()
        elif self.plot == 'INDP':
            self.indp()
        elif self.plot == 'NETEX':
            self.netex()
        else:
            print("Incorrect Command")

