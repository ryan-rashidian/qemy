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
    """SEC companyfacts bulk downloader.

    Downloads all CIK##########.json files and CIK mapping from SEC.
    Replaces any previously downloaded data.
    """
    bulk_dir = cfg.BULK_DIR
    companyfacts_zip = bulk_dir / "companyfacts.zip"
    companyfacts_unzipped = bulk_dir / "companyfacts"
    cik_tickers_json = bulk_dir / "company_tickers.json"
    headers = {"User-Agent": cfg.edgar_user_agent()}

    # Remove old data
    if companyfacts_unzipped.exists():
        logger.info("Removing old bulk filing data...")
        shutil.rmtree(companyfacts_unzipped)
        logger.info("Old data removed.")

    # Download companyfacts ZIP
    logger.info("Downloading bulk filing data...")
    safe_status_download(
        url=cfg.EDGAR_ZIP_URL,
        headers=headers,
        dest_path=companyfacts_zip
    )
    time.sleep(1) # polite delay

    # Download CIK mapping
    logger.info('Downloading CIK mapping...')
    cik_data = safe_status_get(url=cfg.EDGAR_CIK_URL, headers=headers)
    with open(cik_tickers_json, 'w') as f:
        json.dump(cik_data, f)

    logger.info("Downloads Complete.")

    # Unzip companyfacts
    logger.info("Unzipping file...")
    with zipfile.ZipFile(companyfacts_zip, 'r') as zip_ref:
        zip_ref.extractall(companyfacts_unzipped)
    logger.info(f"Unzipped to: {companyfacts_unzipped.resolve()}")

