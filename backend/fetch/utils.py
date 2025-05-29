from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

def parse_period(period_str):
    now = datetime.now()
    unit = period_str[-1].upper()
    value = int(period_str[:-1])

    if unit == 'D':
        start_date = now - relativedelta(days=value)
    elif unit == 'W':
        start_date = now - relativedelta(weeks=value)
    elif unit == "M":
        start_date = now - relativedelta(months=value)
    elif unit == "Y":
        start_date = now - relativedelta(years=value)
    else:
        raise ValueError("Invalid period format. Use D, W, M, or Y")

    return start_date.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d')

def safe_status_get(url, headers=None, params=None):
    response = None
    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        status = response.status_code if response else 'No code'
        body = response.text if response else 'No response'
        print(f"HTTP error {status}: {body}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

