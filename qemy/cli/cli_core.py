from numbers import Number
from qemy.utils.utils_cli import save_to_csv
from qemy.utils.parse_arg import parse_args
from qemy.core.watch_list import WatchListManager
from qemy.cli.cli_helper import print_help_table

#================================== CORE =====================================#

def watch_list(arg, ticker_list):
    help, = parse_args(arg_str=arg, expected_args=['help'], prog_name='watchlist')

    if help:
        return print_help_table(" wl ", [
            ("Info:", "Launches Watchlist manager"),
            ("Usage:", "qemy> wl"),
            ("Commands:", ""),
            ("'add'", "add <TICKER>"),
            ("'remove'", "remove <TICKER>"),
            ("'show'", "Shows current Watchlist"),
            ("'exit', 'q'", "Exits Watchlist manager"),
            ("Example:", "qemy>wl> add <TICKER>\n"),
        ])
    else:
        WatchListManager(ticker_list=ticker_list).run()

def table(arg, ticker_df):
    save_state, help = parse_args(arg_str=arg, expected_args=['save', 'help'], prog_name='table')

    if help:
        return print_help_table(" table ", [
            ("Info:", "Displays a table of every filing fetched during current session."), 
            ("-s --save", "Saves current working table as a .csv file."),
            ("Usage:", "qemy> table"),
            ("Example:", "qemy> table -s\n"),
        ])

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

