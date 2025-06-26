from qemy.core.metric import value, risk
from qemy.utils.parse_arg import parse_args_cli, check_help
from qemy.cli.cli_helper import print_help_table

class RatiosCmd:
    def __init__(self, arg):
        self.help_requested = False
        self.failed = False

        if check_help(
            arg_str=arg, 
            help_func=lambda: print_help_table(" ratio commands ", [
                ("pe", "P/E Ratio"),
                ("pb", "P/B Ratio"),
                ("sharpe", "Sharpe Ratio"),
                ("For More Info:", "ratio <COMMAND> -h\n"),
            ])
        ):
            self.help_requested = True
            return

        core_args, plugin_kwargs, other_args = parse_args_cli(
            arg_str=arg, 
            expected_args=['metric_p', 'ticker_flag', 'period', 'help'], 
            prog_name='ratios', 
        )

        if plugin_kwargs or other_args:
            print(f"Unexpected command: {other_args} {plugin_kwargs}")
            self.failed = True
            return

        self.metric, self.ticker, self.period, self.help = core_args

    def _pe(self):
        if self.help:
            print_help_table(" pe ", [
                ("Info:", "Fetches P/E ratio for given ticker"),
                ("Usage:", "ratio pe -t <TICKER>\n"),
            ])
        else:
            print(value.ratio_pe(ticker=self.ticker))
    
    def _pb(self):
        if self.help:
            print_help_table(" pb ", [
                ("Info:", "Fetches P/B ratio for given ticker"),
                ("Usage:", "ratio pb -t <TICKER>\n"),
            ])
        else:
            print(value.ratio_pb(ticker=self.ticker))

    def _sharpe(self):
        if self.help:
            print_help_table(" sharpe ", [
                ("Info:", "Fetches Sharpe ratio for given ticker"),
                ("Usage:", "ratio sharpe -t <TICKER> -p <PERIOD>\n"),
            ])
        else:
            print(risk.ratio_sharpe(ticker=self.ticker, period=self.period))
        

    def run(self):
        if self.help_requested or self.failed:
            return

        if self.metric == 'PE':
            self._pe()
        elif self.metric == 'PB':
            self._pb()
        elif self.metric == 'SHARPE':
            self._sharpe()
        else:
            print("Ratio: Incorrect metric")

