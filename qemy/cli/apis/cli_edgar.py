from numbers import Number

import pandas as pd

from qemy.data import EDGARClient

from .._parse_args import check_help, parse_args_cli
from ..core.helper import print_help_table

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# === EDGAR ===

def filing(arg, ticker_df) -> pd.DataFrame | None:
    """Print filing data to CLI.

    Args:
        arg (str): CLI input string
        ticker_df (pd.Dataframe): Holds current CLI session filing history
            - Accessed via 'table' command in CLI

    Returns:
        pd.DataFrame: ticker_df and new filing concatenated together
        None: If --help called or EDGARClient returns None
    """
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" f ", [
            ("Info:", "Fetches SEC filing data for given ticker"),
            ("Usage:", "f <TICKER> -f <STATEMENT>"),
            ("Example:", "f aapl -f balance\n"),
            ("-f --file Commands:", ""),
            ("balance", "- Balance Sheet"),
            ("cashflow", "- Cash Flow Statement"),
            ("income", "- Income Statement"),
            ("concept", "- Given metric from form\n"),
        ])
    ):
        return

    try:
        core_args, plugin_kwargs, other_args = parse_args_cli(
            arg_str=arg,
            expected_args=['ticker', 'request', 'file', 'metric', 'quarter'],
            prog_name='filing',
        )
    except Exception as e:
        print(e)
        return

    if plugin_kwargs or other_args:
        print(f"Unexpected command: {other_args} {plugin_kwargs}")
        return

    ticker, request, file, metric, quarters = core_args

    if not request:
        request = False

    if file == 'BALANCE':
        balance_df = EDGARClient(
            ticker=ticker,
            use_requests=request
        ).get_balance_sheet()
        if balance_df is None or balance_df.empty:
            return None

        print(balance_df.to_string(justify='left', formatters={
            ticker: lambda x: f"{x:,}" if isinstance(x, Number) else x
        }))
        return

    elif file == 'CASHFLOW':
        cashflow_df = EDGARClient(
            ticker=ticker,
            use_requests=request
        ).get_cashflow_statement()
        if cashflow_df is None or cashflow_df.empty:
            return None

        print(cashflow_df.to_string(justify='left', formatters={
            ticker: lambda x: f"{x:,}" if isinstance(x, Number) else x
        }))
        return

    elif file == 'INCOME':
        income_df = EDGARClient(
            ticker=ticker,
            use_requests=request
        ).get_income_statement()
        if income_df is None or income_df.empty:
            return None

        print(income_df.to_string(justify='left', formatters={
            ticker: lambda x: f"{x:,}" if isinstance(x, Number) else x
        }))
        return

    elif file == 'METRIC':
        concept_df = EDGARClient(
            ticker=ticker,
            use_requests=request
        ).get_concept(concept=metric, quarters=int(quarters))
        if concept_df is None or concept_df.empty:
            return None

        concept_df.rename(
            columns={'val': 'Value', 'filed': 'Date', 'form': 'Form'},
            inplace=True
        )
        concept_df.set_index('Date', inplace=True)
        print(concept_df.to_string(justify='left', formatters={
            'Value': lambda x: f"{x:,}" if isinstance(x, Number) else x
        }))
        return

    else:
        filing_df = EDGARClient(
            ticker=ticker,
            use_requests=request
        ).get_filing()
        if filing_df is None or filing_df.empty:
            return None

        ticker_df = pd.concat([ticker_df, filing_df], axis=1)

        print(filing_df.to_string(justify='left', formatters={
            ticker: lambda x: f"{x:,}" if isinstance(x, Number) else x
        }))
        if isinstance(ticker_df, pd.DataFrame):
            return ticker_df
        else:
            return None

