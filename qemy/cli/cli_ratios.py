from qemy.core.metric import ratios as rat
from qemy.utils.parse_arg import parse_args_cli, check_help
from qemy.cli.cli_helper import print_help_table

class RatiosCmd:
    def __init__(self, arg):
        self.help_requested = False
        self.failed = False

        if check_help(
            arg_str=arg, 
            help_func=lambda: print_help_table(" ratio commands ", [
                ("pe", ""),
                ("For More Info:", "ratio <COMMAND> -h\n"),
            ])
        ):
            self.help_requested = True
            return

        core_args, plugin_kwargs, other_args = parse_args_cli(
            arg_str=arg, 
            expected_args=['metric_p', 'ticker_flag', 'help'], 
            prog_name='ratios', 
        )

        if plugin_kwargs or other_args:
            print(f"Unexpected command: {other_args} {plugin_kwargs}")
            self.failed = True
            return

        self.metric, self.ticker, self.help = core_args

    def _pe(self):
        if self.help:
            print_help_table(" pe ", [
                ("Info:", "Fetches P/E ratio for given ticker"),
                ("Usage:", "ratio pe -t <TICKER>\n"),
            ])
        else:
            print(rat.ratio_pe(ticker=self.ticker))

    def run(self):
        if self.help_requested or self.failed:
            return

        if self.metric == 'PE':
            self._pe()
        else:
            print("Ratio: Incorrect metric")

