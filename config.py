import os

FRED_API_KEY = os.getenv('FRED_API_KEY')
TIINGO_API_KEY = os.getenv('TIINGO_API_KEY')
EDGAR_USER_AGENT = os.getenv('EDGAR_USER_AGENT')

FRED_URL = "https://api.stlouisfed.org/fred/series/observations"
TIINGO_URL = "https://api.tiingo.com/tiingo/daily/"
TIINGO_IEX_URL = "https://api.tiingo.com/iex/"
EDGAR_CIK_URL = "https://www.sec.gov/files/company_tickers.json"
EDGAR_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK"
EDGAR_ZIP_URL = "https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip"

