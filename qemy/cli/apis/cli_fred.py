from ..core.helper import print_help_table
from .._parse_args import check_help, parse_args_cli

from qemy.data import FREDClient

# === FRED ===

class FREDCmd:
    def __init__(self, arg):
        self.help_requested = False
        self.failed = False
        self.metric = None

        if check_help(
            arg_str=arg, 
            help_func=lambda: print_help_table(" fred commands ", [
                ("cpi", ""),
                ("gdp", ""),
                ("indp", ""),
                ("interest", ""),
                ("jobc", ""),
                ("netex", ""),
                ("nfp", ""),
                ("rfr", ""),
                ("sent", ""),
                ("unem", ""),
                ("For More Info:", "fred <COMMAND> -h\n"),
            ])
        ):
            self.help_requested = True
            return

        try:
            core_args, plugin_kwargs, other_args = parse_args_cli(
                arg_str=arg, 
                expected_args=['metric_p', 'period', 'units', 'help'], 
                prog_name='fred'
            )
            if plugin_kwargs or other_args:
                print(f"Unexpected command: {other_args} {plugin_kwargs}")
                self.failed = True
                return

            self.metric, self.period, self.units, self.help = core_args

        except:
            return

    def rfr(self):
        if self.help:
            print_help_table(" rfr ", [
                ("Info:", "Fetches 1 Year TBill Yield"),
                ("Usage:", "fred rfr\n")
            ])

        else:
            try:
                print(FREDClient().get_tbill_yield())
            except Exception as e:
                print(f"Could not fetch data ERROR:\n{e}")

    def cpi(self):
        if self.help:
            print_help_table(" cpi ", [
                ("Info:", "Fetches Consumer Price Index data"),
                ("Usage:", "fred cpi -p <PERIOD>\n"),
            ])

        else:
            units = 'pc1' if self.units is None else self.units
            if isinstance(self.period, str):
                try:
                    print(FREDClient().get_cpi(period=self.period, units=units))
                except Exception as e:
                    print(f"Could not fetch data ERROR:\n{e}")
            else:
                print('For valid syntax, Try: cpi -p 1Y')

    def gdp(self):
        if self.help:
            print_help_table(" gdp ", [
                ("Info:", "Fetches Gross Domestic Product data"),
                ("Usage:", "fred gpd -p <PERIOD>\n"),
            ])

        else:
            units = 'pc1' if self.units is None else self.units
            if isinstance(self.period, str):
                try:
                    print(FREDClient().get_gdp(period=self.period, units=units))
                except Exception as e:
                    print(f"Could not fetch data ERROR:\n{e}")
            else:
                print('For valid syntax, Try: gdp -p 1Y')

    def sent(self):
        if self.help:
            print_help_table(" sent ", [
                ("Info:", "Fetches Consumer Sentiment Index data"),
                ("Usage:", "fred sent -p <PERIOD>\n"),
            ])

        else:
            units = 'pch' if self.units is None else self.units
            if isinstance(self.period, str):
                try:
                    print(FREDClient().get_sentiment(period=self.period, units=units))
                except Exception as e:
                    print(f"Could not fetch data ERROR:\n{e}")
            else:
                print('For valid syntax, Try: sent -p 1Y')

    def nfp(self):
        if self.help:
            print_help_table(" nfp ", [
                ("Info:", "Fetches Nonfarm Payroll data"),
                ("Usage:", "fred nfp -p <PERIOD>\n"),
            ])

        else:
            units = 'pc1' if self.units is None else self.units
            if isinstance(self.period, str):
                try:
                    print(FREDClient().get_nf_payrolls(period=self.period, units=units))
                except Exception as e:
                    print(f"Could not fetch data ERROR:\n{e}")
            else:
                print('For valid syntax, Try: nfp -p 1Y')

    def interest(self):
        if self.help:
            print_help_table(" interest ", [
                ("Info:", "Fetches Fed Interest Rate data"),
                ("Usage:", "fred interest -p <TICKER>\n"),
            ])

        else:
            units = 'pc1' if self.units is None else self.units
            if isinstance(self.period, str):
                try:
                    print(FREDClient().get_interest_rate(period=self.period, units=units))
                except Exception as e:
                    print(f"Could not fetch data ERROR:\n{e}")
            else:
                print('For valid syntax, Try: interest -p 1Y')

    def jobc(self):
        if self.help:
            print_help_table(" jobc ", [
                ("Info:", "Fetches Jobless Claim data"),
                ("Usage:", "fred jobc -p <PERIOD>\n"),
            ])

        else:
            units = 'pc1' if self.units is None else self.units
            if isinstance(self.period, str):
                try:
                    print(FREDClient().get_jobless_claims(period=self.period, units=units))
                except Exception as e:
                    print(f"Could not fetch data ERROR:\n{e}")
            else:
                print('For valid syntax, Try: jobc -p 1Y')

    def unem(self):
        if self.help:
            print_help_table(" unem ", [
                ("Info:", "Fetches Unemployment Rate data"),
                ("Usage:", "fred unem -p <PERIOD>\n"),
            ])

        else:
            units = 'pc1' if self.units is None else self.units
            if isinstance(self.period, str):
                try:
                    print(FREDClient().get_unemployment(period=self.period, units=units))
                except Exception as e:
                    print(f"Could not fetch data ERROR:\n{e}")
            else:
                print('For valid syntax, Try: unem -p 1Y')

    def indp(self):
        if self.help:
            print_help_table(" indp ", [
                ("Info:", "Fetches Industrial Production data"),
                ("Usage:", "fred indp -p <PERIOD>\n"),
            ])

        else:
            units = 'pc1' if self.units is None else self.units
            if isinstance(self.period, str):
                try:
                    print(FREDClient().get_industrial_production(period=self.period, units=units))
                except Exception as e:
                    print(f"Could not fetch data ERROR:\n{e}")
            else:
                print('For valid syntax, Try: indp -p 1Y')

    def netex(self):
        if self.help:
            print_help_table(" netex ", [
                ("Info:", "Fetches Net Export data"),
                ("Usage:", "fred netex -p <PERIOD>\n"),
            ])

        else:
            units = 'lin' if self.units is None else self.units 
            if isinstance(self.period, str):
                try:
                    print(FREDClient().get_net_exports(period=self.period, units=units.lower()))
                except Exception as e:
                    print(f"Could not fetch data ERROR:\n{e}")
            else:
                print('For valid syntax, Try: netex -p 1Y')

    def run(self):
        if self.help_requested or self.failed or self.metric is None:
            return

        if self.metric == 'RFR':
            self.rfr()
        elif self.metric == 'CPI':
            self.cpi()
        elif self.metric == 'GDP':
            self.gdp()
        elif self.metric == 'SENT':
            self.sent()
        elif self.metric == 'NFP':
            self.nfp()
        elif self.metric == 'INTEREST':
            self.interest()
        elif self.metric == 'JOBC':
            self.jobc()
        elif self.metric == 'UNEM':
            self.unem()
        elif self.metric == 'INDP':
            self.indp()
        elif self.metric == 'NETEX':
            self.netex()
        else:
            print("Incorrect Command")

