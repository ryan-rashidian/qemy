import pandas as pd
from numbers import Number
from qemy.utils.parse_arg import parse_args_cli, check_help
from qemy.data.api_edgar import SEC_Filings
from qemy.cli.cli_helper import print_help_table

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#================================== EDGAR ====================================#

def filing(arg, ticker_df) -> pd.DataFrame | None:
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" f ", [
            ("Info:", "Fetches SEC filing data for given ticker"),
            ("Usage:", "f <TICKER>\n"),
        ])
    ):
        return

    core_args, plugin_kwargs, other_args = parse_args_cli(
        arg_str=arg, 
        expected_args=['ticker', 'request'], 
        prog_name='filing', 
    )

    if plugin_kwargs or other_args:
        print(f"Unexpected command: {other_args} {plugin_kwargs}")
        return

    ticker, request = core_args

    if not request:
        request = False

    if isinstance(ticker, str):
        print(f"Fetching latest 10K/10Q/20F filing metrics for {ticker}")

        try:
            filing_df = SEC_Filings(ticker=ticker, use_requests=request).get_metrics() 
            if isinstance(filing_df, pd.DataFrame): 
                ticker_df[ticker] = filing_df[ticker]
                print(filing_df.to_string(justify='left', formatters={
                    ticker: lambda x: f"{x:,}" if isinstance(x, Number) else x
                }))
                if isinstance(ticker_df, pd.DataFrame):
                    return ticker_df
                else:
                    return None
        except:
            print("cli_edgar\nCould not fetch filing metrics, try another ticker.")

    else:
        print(f"failed to find {ticker}")

def filing_metric(arg):
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" fmetric ", [
            ("Info:", "Fetches SEC filing data for given ticker and metric"),
            ("Usage:", "fmetric <TICKER> -m <METRIC>\n"),
        ])
    ):
        return

    core_args, plugin_kwargs, other_args = parse_args_cli(
        arg_str=arg, 
        expected_args=['ticker', 'quarter', 'metric'], 
        prog_name='fmetric', 
    )

    if plugin_kwargs or other_args:
        print(f"Unexpected command: {other_args} {plugin_kwargs}")
        return

    ticker, quarters, metric = core_args

    if isinstance(ticker, str) and isinstance(metric, str) and quarters:

        try:
            metric.strip().lower()
            ticker = ticker.strip()
            quarters = int(quarters)
            metric_df = SEC_Filings(ticker=ticker).get_metric_history(quarters=quarters, key=metric)
            if isinstance(metric_df, pd.DataFrame): 
                metric_df['pch'] = metric_df['val'].pct_change().map(lambda x: f"{x:.2%}" if pd.notnull(x) else "0.00%") 
                total_pch = (metric_df['val'].iloc[-1] - metric_df['val'].iloc[0]) / metric_df['val'].iloc[0]
                print(metric_df.to_string(justify='left', formatters={
                    ticker: lambda x: f"{x:,}" if isinstance(x, Number) else x
                }))
                print(f"\nTotal % Change: {total_pch:.2%}")
        except:
            print("cli_edgar\nCould not fetch metric, try another ticker")

    else:
        print("For valid syntax, try: fmetric -t <TICKER> -q 20 -m EPS")

