"""SEC bulk downloader."""

import json
import logging
import shutil
import time
import zipfile

from qemy import _config as cfg
from qemy.data._api_tools import safe_status_download, safe_status_get

logger = logging.getLogger(__name__)

def bulk_refresh():
    """SEC companyfacts.zip bulk downloader function.

    Downloads all available CIK##########.json files from SEC servers.
    It will also replace any previously downloaded data.

    The SEC updates their bulk data nightly.
    """
    bulk_dir = cfg.BULK_DIR

    unzipped_dir = bulk_dir / "companyfacts"
    if unzipped_dir.exists() and unzipped_dir.is_dir():
        logger.info("Removing old bulk filing data...")
        shutil.rmtree(unzipped_dir)
        logger.info("Removed.")

    companyfacts_url = cfg.EDGAR_ZIP_URL
    cik_tickers_url = cfg.EDGAR_CIK_URL
    companyfacts_zip = bulk_dir / "companyfacts.zip"
    cik_tickers_json = bulk_dir / "company_tickers.json"
    headers = {"User-Agent": cfg.edgar_user_agent()}

    logger.info("Downloading bulk filing data...")
    safe_status_download(
        url=companyfacts_url,
        headers=headers,
        dest_path=companyfacts_zip
    )

    time.sleep(1) # be polite to SEC server

    cik_data = safe_status_get(url=cik_tickers_url, headers=headers)
    if cik_data is None:
        logger.error("Download failed for company_tickers.json")
    with open(cik_tickers_json, 'w') as f:
        json.dump(cik_data, f)
    logger.info("Download Complete.\n")

    logger.info("Unzipping file...")
    companyfacts_unzipped = bulk_dir / "companyfacts"
    with zipfile.ZipFile(companyfacts_zip, 'r') as zip_ref:
        zip_ref.extractall(companyfacts_unzipped)
    logger.info(f"Unzipped to: {companyfacts_unzipped.resolve()}")

