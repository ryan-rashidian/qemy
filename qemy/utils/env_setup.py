import sys
from pathlib import Path
from dotenv import load_dotenv

def setup_input(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() in ('exit', 'q'):
        sys.exit()
    else:
        return user_input

def setup_wizard():
    if getattr(sys, 'frozen', False):
        project_root = Path(sys.executable).resolve().parent
    else:
        project_root = Path(__file__).resolve().parents[2]
    env_path = project_root / '.env'
    temp_env_path = project_root / '.env.tmp'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        return

    print("\n No .env file found!\n Please setup your FRED API key, Tiingo API key, and EDGAR API 'User Agent'")
    print(" Type: 'exit' or 'q' to exit this setup at any time.")

    try:
        fred_key = setup_input(" Enter your FRED API key: ")
        tiingo_key = setup_input(" Enter your Tiingo API key: ")
        print(" Enter a 'User Agent' to identify yourself to EDGAR API")
        print(" - e.g. john johndoe@example.com")
        edgar_agent = setup_input("Enter a 'User Agent': ")
        with temp_env_path.open('w') as f:
            f.write(f"FRED_API_KEY={fred_key}\n")
            f.write(f"TIINGO_API_KEY={tiingo_key}\n")
            f.write(f"EDGAR_USER_AGENT={edgar_agent}\n")
        temp_env_path.rename(env_path)
        print(
            " .env file created successfully!\n",
            "\n Tip: use the bulk_refresh command to download SEC filings locally on your machine.\n",
            "    - This is faster and helps avoid hitting SEC rate limits.\n",
            "    - Otherwise, use '-r' or '--request' flags to fetch indicidual filings live.\n"
            "      Be mindful of your usage - the SEC discourages frequent scraping.\n"
        )
        load_dotenv(dotenv_path=env_path)
    except SystemExit:
        if temp_env_path.exists():
            temp_env_path.unlink()
        print("Setup aborted. No setup information saved.\n")
        sys.exit()

