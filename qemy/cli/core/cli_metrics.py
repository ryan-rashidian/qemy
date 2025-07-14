from qemy.core.metrics import growth, risk, value

from .._parse_args import check_help, parse_args_cli
from .helper import print_help_table


class MetricCmd:
    def __init__(self, arg):
        self.help_requested = False
        self.failed = False

        if check_help(
            arg_str=arg,
            help_func=lambda: print_help_table(" metric Commands ", [
                ("pe", "P/E Ratio"),
                ("pb", "P/B Ratio"),
                ("sharpe", "Sharpe Ratio"),
                ("maxdd", "Max Drawdown"),
                ("vol", "Volatility"),
                ("cagr", "Compounded Annual Growth Rate\n"),
                ("PCH Commands:", "shares, cash, debt, netdebt, rev, cogs"),
                ("", "gprofit, ebit, netinc, assets, liab"),
                ("", "equity, opex, capex, ocf, fcf, eps\n"),
                ("For More Info:", "metric <COMMAND> -h\n"),
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
                ("Usage:", "metric pe -t <TICKER>\n"),
            ])

        else:
            results_dict = value.ratio_pe(ticker=self.ticker)
            print(f"Ticker: {self.ticker}")
            print(f"Price: {results_dict['price']:.2f}")
            print(f"TTM EPS: {results_dict['ttm_eps']:.2f}")
            print(f"P/E Ratio: {results_dict['pe']}")

    def _pb(self):
        if self.help:
            print_help_table(" pb ", [
                ("Info:", "Fetches P/B ratio for given ticker"),
                ("Usage:", "metric pb -t <TICKER>\n"),
            ])

        else:
            results_dict = value.ratio_pb(ticker=self.ticker)
            print(f"Ticker: {self.ticker}")
            print(f"Price: {results_dict['price']}")
            print(f"BVPS: {results_dict['bvps']}")
            print(f"P/B Ratio: {results_dict['pb']}")

    def _sharpe(self):
        if self.help:
            print_help_table(" sharpe ", [
                ("Info:", "Fetches Sharpe ratio for given ticker"),
                ("Usage:", "metric sharpe -t <TICKER> -p <PERIOD>\n"),
            ])

        else:
            results_dict = risk.ratio_sharpe(
                ticker=self.ticker,
                period=self.period
            )
            print(f"Ticker: {self.ticker}")
            print(f"RFR: {results_dict['rfr']:.3f}")
            print(f"1 Year Mean: {results_dict['mean']:.3f}")
            print(f"1 Year STD: {results_dict['std']:.3f}")
            print(f"Sharpe Ratio: {results_dict['sharpe']:.2f}")

    def _maxdd(self):
        if self.help:
            print_help_table(" maxdd ", [
                ("Info:", "Fetches Max Drawdown"),
                ("Usage:", "metric maxdd -t <TICKER> -p <PERIOD>\n"),
            ])

        else:
            results_dict = risk.max_dd(
                ticker=self.ticker,
                period=self.period
            )
            print(f"Ticker: {self.ticker}")
            print(f"Max Drawdown: {results_dict['maxdd']:.2%}")

    def _volatility(self):
        if self.help:
            print_help_table(" vol ", [
                ("Info:", "Fetches Annualized Volatility"),
                ("Usage:", "metric vol -t <TICKER> -p <PERIOD>\n"),
            ])

        else:
            results_dict = risk.volatility(
                ticker=self.ticker,
                period=self.period
            )
            print(f"Ticker: {self.ticker}")
            print(f"Volatility: {results_dict['vol']:.2%} Annualized")


    def _cagr(self):
        if self.help:
            print_help_table(" cagr ", [
                ("Info:", "Fetches Compounded Annual Growth Rate"),
                ("Usage:", "metric cagr -t <TICKER> -p <PERIOD>\n"),
            ])

        else:
            results_dict = growth.cagr(
                ticker=self.ticker,
                period=self.period
            )
            print(f"Ticker: {self.ticker}")
            print(f"CAGR: {results_dict['cagr']:.2%} Annualized")

    def _growth(self):
        if self.help:
            print_help_table(f" {self.metric} ", [
                ("Info:", f"Fetches yearly {self.metric.upper()} growth rate"),
                ("Usage:", f"metric {self.metric.upper()} -t <TICKER>\n"),
            ])

        else:
            results_dict = growth.growth_rate(
                ticker=self.ticker,
                metric=self.metric
            )

            print(f"Ticker: {self.ticker}")
            print(
                f"{self.metric} Growth: "
                f"{results_dict['growth']:.2%} Annualized"
            )

    def run(self):
        if self.help_requested or self.failed:
            return

        if self.metric == 'PE':
            self._pe()
        elif self.metric == 'PB':
            self._pb()
        elif self.metric == 'SHARPE':
            self._sharpe()
        elif self.metric == 'MAXDD':
            self._maxdd()
        elif self.metric == 'VOL':
            self._volatility()
        elif self.metric == 'CAGR':
            self._cagr()
        elif self.metric in (
                'SHARES', 'CASH', 'DEBT', 'NETDEBT', 'REV', 'COGS',
                'GPROFIT', 'EBIT', 'NETINC', 'ASSETS', 'LIAB',
                'EQUITY', 'OPEX', 'CAPEX', 'OCF', 'FCF', 'EPS',
            ):
            self._growth()

        else:
            print("metric: Incorrect metric")

