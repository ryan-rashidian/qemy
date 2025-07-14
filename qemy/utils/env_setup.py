"""Environment Setup Wizard for Qemy CLI."""

import sys

from dotenv import load_dotenv

from qemy import _config as cfg


def _setup_input(prompt: str) -> str:
    """Prompt the user for input. Exits if input is 'exit' or 'q'.

    Args:
        prompt (str): The message displayed to users

    Returns:
        str: The stripped user input
    """
    user_input = input(prompt).strip()

    if user_input.lower() in ('exit', 'q'):
        sys.exit()
    else:
        return user_input

def setup_wizard():
    """Setup Wizard to initialize environment variables.

    Prompts the user for API credentials and stores them in .env file.
    If .env already exists, it will just load the environment variables.
    """
    project_root = cfg.PROJECT_ROOT

    env_path = project_root / '.env'
    temp_env_path = project_root / '.env.tmp'

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        return

    print("\n No .env file found!")
    print(" Please setup your API credentials.")
    print(" Type: 'exit' or 'q' to exit this setup at any time.")

    try:
        fred_key = _setup_input(" Enter your FRED API key: ")
        tiingo_key = _setup_input(" Enter your Tiingo API key: ")
        print(" Enter a 'User Agent' to identify yourself to EDGAR API")
        print(" - e.g. john johndoe@example.com")
        edgar_agent = _setup_input("Enter a 'User Agent': ")

        with temp_env_path.open('w') as f:
            f.write(f"FRED_API_KEY={fred_key}\n")
            f.write(f"TIINGO_API_KEY={tiingo_key}\n")
            f.write(f"EDGAR_USER_AGENT={edgar_agent}\n")

        temp_env_path.rename(env_path)

        print(
            " .env file created successfully!\n",
            "\n Tip: use the bulk_refresh command to download SEC filings.\n",
            "    - This is faster and helps avoid hitting SEC rate limits.\n",
            "    - Otherwise, use '-r' or '--request' flag.\n"
            "      Be mindful of your request usage.\n"
        )

        load_dotenv(dotenv_path=env_path)

    except SystemExit:
        if temp_env_path.exists():
            temp_env_path.unlink()

        print("Setup aborted. No setup information saved.\n")
        sys.exit()

