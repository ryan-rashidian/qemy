import logging
import sys
from pathlib import Path

from qemy.data import bulk_refresh as bulk_r

from .._parse_args import check_help
from ..core.helper import print_help_table


def bulk_refresh(arg):
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" bulk_refresh ", [
                ("Info:", "Download, or refresh existing SEC filing data"),
                ("Size:", "~18GB\n"),
        ])
    ):
        return

    confirm = input(
        "All previous bulk data will be overwritten.\n"
        "Are you sure? (yes/no): "
    )
    if confirm.strip().lower() == 'yes':
        try:
            bulk_r()
        except Exception as e:
            print(f"cli_edgar\nBulk refresh failed. Error:\n{e}")

def calc(arg):
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" calc ", [
            ("Info:", "Simple calculator with Python syntax"),
            ("Example:", "calc 2 + 2\n"),
        ])
    ):
        return

    try:
        result = eval(arg, {"__builtins__": {}}, {})
        print(result)
    except Exception as e:
        print(f"Invalid expression\n{e}")

def debug(arg: str, debug_mode: bool) -> bool | None:
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" debug ", [
            ("Info:", "Toggles log messages in CLI\n"),
        ])
    ):
        return

    if debug_mode:
        logging.disable(logging.CRITICAL + 1)
        print("Logging is now OFF")
        debug_mode = False
        return debug_mode

    else:
        logging.disable(logging.NOTSET)
        print("Logging is now ON")
        debug_mode = True
        return debug_mode

def env_reset(arg):
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" env_reset ", [
            ("Info:", "Delete current API key setup"),
            ("", "(Removed .env file from Qemy)"),
            ("", "Restarts current Qemy CLI session\n"),
        ])
    ):
        return

    if getattr(sys, 'frozen', False):
        project_root = Path(sys.executable).resolve().parent
    else:
        project_root = Path(__file__).resolve().parents[2]

    env_path = project_root / '.env'

    confirm = input(
        "Are you sure you want to delete the .env file?\n"
        "This action will also exit qemy. (yes/no): "
    ).strip().lower()
    if confirm != 'yes':
        print("Aborted. .env file was not deleted.\n")
        return

    if env_path.exists():
        env_path.unlink()
        print(".env file deleted. Exiting qemy...\n")
        sys.exit()
    else:
        print("No .env file found. Nothing to delete.\n")
        return

