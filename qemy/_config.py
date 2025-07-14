import sys
from pathlib import Path

from dotenv import load_dotenv

from qemy.utils.env_tools import get_env_str

# === KEY ===

dotenv_path = Path(__file__).resolve().parents[1] / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)

# Lazy accessors for API keys
def fred_api_key() -> str:
    return get_env_str('FRED_API_KEY')

def tiingo_api_key() -> str:
    return get_env_str('TIINGO_API_KEY')

def edgar_user_agent() -> str:
    return get_env_str('EDGAR_USER_AGENT')

# === URL ===

FRED_URL = "https://api.stlouisfed.org/fred/series/observations"

TIINGO_URL = "https://api.tiingo.com/tiingo/daily/"
TIINGO_IEX_URL = "https://api.tiingo.com/iex/"

EDGAR_CIK_URL = "https://www.sec.gov/files/company_tickers.json"
EDGAR_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK"
EDGAR_ZIP_URL = "https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip"

# === PATH ===

# Check if executable before determining root path
if getattr(sys, 'frozen', False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPORT_CHART_DIR = PROJECT_ROOT / "exports" / "charts"
EXPORT_CHART_DIR.mkdir(parents=True, exist_ok=True)

EXPORT_TABLE_DIR = PROJECT_ROOT / "exports" / "tables"
EXPORT_TABLE_DIR.mkdir(parents=True, exist_ok=True)

BULK_DIR = PROJECT_ROOT / "bulk_data"
BULK_DIR.mkdir(parents=True, exist_ok=True)

