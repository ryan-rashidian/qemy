from numbers import Number

from qemy.utils.file_tools import save_to_csv

from .._parse_args import check_help, parse_args_cli
from ..core.helper import print_help_table
from ._watchlist import WatchListManager

# === CORE ===

def watch_list(arg, ticker_list):
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" wl ", [
            ("Info:", "Launches Watchlist manager"),
            ("Usage:", "qemy> wl"),
            ("Commands:", ""),
            ("'add'", "add <TICKER>"),
            ("'remove'", "remove <TICKER>"),
            ("'show'", "Shows current Watchlist"),
            ("'exit', 'q'", "Exits Watchlist manager"),
            ("Example:", "qemy>wl> add <TICKER>\n"),
        ])
    ):
        return

    WatchListManager(ticker_list=ticker_list).run()

def table(arg, ticker_df):
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" table ", [
            ("Info:", "Displays all filings fetched from current session."),
            ("-s --save", "Saves current working table as a .csv file."),
            ("Usage:", "qemy> table\n"),
        ])
    ):
        return

    core_args, plugin_kwargs, other_args = parse_args_cli(
        arg_str=arg,
        expected_args=['save'],
        prog_name='table'
    )

    if plugin_kwargs or other_args:
        print(f"Unexpected command: {other_args} {plugin_kwargs}")
        return

    save_state, = core_args
    try:
        if save_state:
            save_to_csv(df=ticker_df)
            print("File saved...\n /qemy/exports/tables/")
        else:
            print('Filings:')
            print(ticker_df.to_string(justify='left', formatters={
                col: (lambda x: f"{x:,}" if isinstance(x, Number) else x)
                for col in ticker_df.columns
            }))
    except Exception as e:
        print(f"Could not fetch/save table. ERROR:\n{e}")

