import os
import time
import shutil
import zipfile
import json
from pathlib import Path
from .utils_fetch import safe_status_get, safe_status_download

def bulk_refresh():
    bulk_dir = Path("bulk_data")
    bulk_dir.mkdir(exist_ok=True)

    unzipped_dir = bulk_dir / "companyfacts"
    if unzipped_dir.exists() and unzipped_dir.is_dir():
        print("Removing old bulk filing data...")
        shutil.rmtree(unzipped_dir)
        print("Removed.")

    companyfacts_url = "https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip"
    cik_tickers_url = "https://www.sec.gov/files/company_tickers.json"
    companyfacts_zip = bulk_dir / "companyfacts.zip"
    cik_tickers_json = bulk_dir / "company_tickers.json"
    headers = {"User-Agent": os.getenv('EDGAR_USER_AGENT')} 

    print("Downloading bulk filing data...")
    success = safe_status_download(url=companyfacts_url, headers=headers, dest_path=companyfacts_zip)
    if not success:
        print("Download failed for companyfacts.zip")

    time.sleep(1) # be polite to SEC server

    cik_data = safe_status_get(url=cik_tickers_url, headers=headers)
    if cik_data is None:
        print("Download failed for company_tickers.json")
    with open(cik_tickers_json, 'w') as f:
        json.dump(cik_data, f)
    print("Download Complete.\n")

    print("Unzipping file...")
    companyfacts_unzipped = bulk_dir / "companyfacts"
    with zipfile.ZipFile(companyfacts_zip, 'r') as zip_ref:
        zip_ref.extractall(companyfacts_unzipped)
    print(f"Unzipped to: {companyfacts_unzipped.resolve()}")

