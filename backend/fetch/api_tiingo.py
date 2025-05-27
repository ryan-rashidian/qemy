import os
import requests 
from .utils import parse_period

TIINGO_API_KEY = os.getenv('TIINGO_API_KEY')
TIINGO_HEADERS = {'Content-Type': 'application/json', 'Authorization': f'Token {TIINGO_API_KEY}'}

def get_tiingo_prices(ticker, period='1W', resample='daily', columns='close'):
    try:
        start_date, end_date = parse_period(period)
        url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices'
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'resampleFreq': resample,
            'columns': columns
        }
        response = requests.get(url=url, headers=TIINGO_HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Data not available for '{ticker}'")
        return None
    except Exception as e:
        print('An error occured: ', e)
        return None

