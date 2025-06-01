from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
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
        raise ValueError("Invalid period format.\nUse: D, W, M, or Y")

    return start_date.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d')

def safe_status_get(url, headers=None, params=None):
    response = None
    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed:\n{e}")
    except Exception as e:
        print(f"Error: {e}")
    return None

def safe_status_download(url, headers=None, dest_path=None):
    if not isinstance(dest_path, Path):
        print("Download failed: dest_path must be valid Path object")
        return False
    try:
        with requests.get(url=url, headers=headers, stream=True) as r:
            r.raise_for_status()
            if isinstance(dest_path, Path):
                with open(dest_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        return True
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return False

