import os
import pandas as pd
from datetime import date, timedelta
from .utils_fetch import parse_period, safe_status_get

FRED_API_KEY = os.getenv('FRED_API_KEY')

def get_tbill_yield():
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'GS1',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': 1,
        'observation_start': start_date.isoformat(),
        'observation_end': end_date.isoformat(),
    }
    try:
        data = safe_status_get(url=url, params=params)
        if data:
            tbill = data['observations'][0] 
            return tbill['value']
    except Exception as e:
        print(f"Failed to request data. Error code:\n{e}")

def get_cpi_inflation(period="1Y"):
    start_date, end_date = parse_period(period)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'CPIAUCSL',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': 'm',
        'aggregation_method': 'avg',
        'units': 'pc1'
    }
    try:
        data = safe_status_get(url=url, params=params)
        if data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df['value'] = df['value'].astype(float)
            df = df.drop('realtime_start', axis=1)
            df = df.drop('realtime_end', axis=1)
            return df
    except Exception as e:
        print(f"Failed to request data. Error code:\n{e}")

def get_gdp(period='1Y'):
    start_date, end_date = parse_period(period)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'GDP',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': 'q',
        'units': 'pc1'
    }
    try:
        data = safe_status_get(url=url, params=params)
        if data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df['value'] = df['value'].astype(float)
            df = df.drop('realtime_start', axis=1)
            df = df.drop('realtime_end', axis=1)
            return df
    except Exception as e:
        print(f"Failed to request data. Error code:\n{e}")

def get_sentiment(period='1Y'):
    start_date, end_date = parse_period(period)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'UMCSENT',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': 'm',
        'units': 'pch'
    }
    try:
        data = safe_status_get(url=url, params=params)
        if data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df['value'] = df['value'].astype(float)
            df = df.drop('realtime_start', axis=1)
            df = df.drop('realtime_end', axis=1)
            return df
    except Exception as e:
        print(f"Failed to request data. Error code:\n{e}")

def get_nf_payrolls(period='1Y'):
    start_date, end_date = parse_period(period)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'PAYEMS',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': 'm',
        'units': 'pc1'
    }
    try:
        data = safe_status_get(url=url, params=params)
        if data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            #df['value'] = df['value'].astype(float)
            df = df.drop('realtime_start', axis=1)
            df = df.drop('realtime_end', axis=1)
            return df
    except Exception as e:
        print(f"Failed to request data. Error code:\n{e}")
        
def get_interest(period='1Y'):
    start_date, end_date = parse_period(period)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'DFF',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': 'd',
        'units': 'pc1'
    }
    try:
        data = safe_status_get(url=url, params=params)
        if data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df['value'] = df['value'].astype(float)
            df = df.drop('realtime_start', axis=1)
            df = df.drop('realtime_end', axis=1)
            return df
    except Exception as e:
        print(f"Failed to request data. Error code:\n{e}")

def get_jobless_claims(period='1Y'):
    start_date, end_date = parse_period(period)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'ICSA',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': 'w',
        'units': 'pc1'
    }
    try:
        data = safe_status_get(url=url, params=params)
        if data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df['value'] = df['value'].astype(float)
            df = df.drop('realtime_start', axis=1)
            df = df.drop('realtime_end', axis=1)
            return df
    except Exception as e:
        print(f"Failed to request data. Error code:\n{e}")

def get_unemployment(period='1Y'):
    start_date, end_date = parse_period(period)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'UNRATE',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': 'm',
        'units': 'pc1'
    }
    try:
        data = safe_status_get(url=url, params=params)
        if data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df['value'] = df['value'].astype(float)
            df = df.drop('realtime_start', axis=1)
            df = df.drop('realtime_end', axis=1)
            return df
    except Exception as e:
        print(f"Failed to request data. Error code:\n{e}")

def get_ind_prod(period='1Y'):
    start_date, end_date = parse_period(period)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'INDPRO',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': 'm',
        'units': 'pc1'
    }
    try:
        data = safe_status_get(url=url, params=params)
        if data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df['value'] = df['value'].astype(float)
            df = df.drop('realtime_start', axis=1)
            df = df.drop('realtime_end', axis=1)
            return df
    except Exception as e:
        print(f"Failed to request data. Error code:\n{e}")

def get_netex(period='1Y'): ### BUG
    start_date, end_date = parse_period(period)
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'NETEXC',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': 'q',
        'units': 'lin'
    }
    try:
        data = safe_status_get(url=url, params=params)
        if data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date']) #### error: 'date' = None, check 'observations' .keys()
            df.set_index('date', inplace=True)
            df['value'] = df['value'].astype(float)
            df = df.drop('realtime_start', axis=1)
            df = df.drop('realtime_end', axis=1)
            return df
    except Exception as e:
        print(f"Failed to request data. Error code:\n{e}")

