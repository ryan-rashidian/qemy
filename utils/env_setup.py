import sys
from pathlib import Path
from dotenv import load_dotenv

def setup_wizard():
    if getattr(sys, 'frozen', False):
        project_root = Path(sys.executable).resolve().parent
    else:
        project_root = Path(__file__).resolve().parent.parent

    env_path = project_root / '.env'

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        return

    print("\n No .env file found! Please setup your Tiingo and FMP API keys.")
    fmp_key = input("Enter your Financial Modeling Prep (FMP) API key: ").strip()
    tiingo_key = input("Enter your Tiingo API key: ").strip()
    with env_path.open('w') as f:
        f.write(f"FMP_API_KEY={fmp_key}\n")
        f.write(f"TIINGO_API_KEY={tiingo_key}\n")
    print(".env file created successfully!\n")
    load_dotenv(dotenv_path=env_path)
