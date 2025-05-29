import os
from .utils_fetch import parse_period, safe_status_get

TIINGO_API_KEY = os.getenv('TIINGO_API_KEY')
TIINGO_HEADERS = {'Content-Type': 'application/json', 'Authorization': f'Token {TIINGO_API_KEY}'}

def get_tiingo_prices(ticker, period='1W', resample='daily', columns='close'):
    start_date, end_date = parse_period(period)
    url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices'
    params = {
        'startDate': start_date,
        'endDate': end_date,
        'resampleFreq': resample,
        'columns': columns
    }
    return safe_status_get(url=url, headers=TIINGO_HEADERS, params=params)

