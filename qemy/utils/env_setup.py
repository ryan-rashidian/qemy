import sys
from pathlib import Path
from dotenv import load_dotenv

def setup_wizard():
    if getattr(sys, 'frozen', False):
        project_root = Path(sys.executable).resolve().parent
    else:
        project_root = Path(__file__).resolve().parents[2]

    env_path = project_root / '.env'

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        return

    print("\n No .env file found! Please setup your FRED API key, Tiingo API key, and EGDAR API 'User Agent'")
    fred_key = input("Enter your FRED API key: ").strip()
    tiingo_key = input("Enter your Tiingo API key: ").strip()
    print("Enter a 'User Agent' to identify yourself to EDGAR API")
    print("- e.g. john johndoe@example.com")
    edgar_agent = input("Enter a 'User Agent': ")
    with env_path.open('w') as f:
        f.write(f"FRED_API_KEY={fred_key}\n")
        f.write(f"TIINGO_API_KEY={tiingo_key}\n")
        f.write(f"EDGAR_USER_AGENT={edgar_agent}\n")
    print(".env file created successfully!\n")
    load_dotenv(dotenv_path=env_path)

