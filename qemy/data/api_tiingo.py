import os
from qemy.utils.utils_fetch import parse_period, safe_status_get

class StockMarket:
    def __init__(self):
        self.API_KEY = os.getenv('TIINGO_API_KEY')
        self.HEADERS = {
            'Content-Type': 'application/json',
            'Authorization': f"Token {self.API_KEY}"
        }

    def get_prices(self, ticker, period='1W', resample='daily', columns='close'):
        start_date, end_date = parse_period(period)
        url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices'
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'resampleFreq': resample,
            'columns': columns
        }
        return safe_status_get(url=url, headers=self.HEADERS, params=params)

    def get_quote(self, tickers):
        if isinstance(tickers, str):
            tickers = [tickers]
        url = f"https://api.tiingo.com/iex/{','.join(tickers)}"
        response = safe_status_get(url=url, headers=self.HEADERS)
        if not isinstance(response, list):
            return {}
        return {entry["ticker"]: entry for entry in response if "ticker" in entry}

