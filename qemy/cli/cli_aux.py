import sys
from pathlib import Path
from qemy.data import api_edgar_bulk as bulk
from qemy.utils.parse_arg import check_help
from qemy.cli.cli_helper import print_help_table

def bulk_refresh(arg):
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" bulk_refresh ", [
                ("Info:", "Download, or refresh current download of SEC filing data"),
                ("Size:", "~18GB\n"),
        ])
    ):
        return

    confirm = input("All previous bulk data will be overwritten.\nAre you sure? (yes/no): ")
    if confirm.strip().lower() == 'yes':
        try:
            bulk.bulk_refresh()
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
    except:
        print("Invalid expression")

def env_reset(arg):
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" env_reset ", [
            ("Info:", "Delete current API key setup (will remove the .env file in project root)"),
            ("", "Will restart current Qemy CLI session, and users will be prompted by the setup wizard on next start\n"),
        ])
    ):
        return

    if getattr(sys, 'frozen', False):
        project_root = Path(sys.executable).resolve().parent
    else:
        project_root = Path(__file__).resolve().parents[2]

    env_path = project_root / '.env'

    confirm = input("Are you sure you want to delete the .env file? This action will also exit qemy. (yes/no): ").strip().lower()
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

