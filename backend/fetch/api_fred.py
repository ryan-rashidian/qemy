import os
import requests

def fredtest():
    FRED_API_KEY = os.getenv('FRED_API_KEY')
    url = 'https://api.stlouisfed.org/fred/series/observations'

    params = {
        'series_id': 'GS1',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': 1
    }

    response = requests.get(url=url, params=params)
    data = response.json()
    tbill = data['observations'][0]
    print(f"1 Year T-Bill Yield: {tbill['value']}%")
