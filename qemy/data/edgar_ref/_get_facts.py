"""Get facts dictionary.

This module contains get_ functions that return companyfacts.
    - Either through requests, or bulk download from SEC EDGAR API.
"""

import json
import logging
import time

from pathlib import Path

from qemy import _config as cfg
from qemy.data._api_tools import safe_status_get
from qemy.exceptions import DataError, InvalidArgumentError

logger = logging.getLogger(__name__)

def _find_cik(ticker: str, cik_data: dict) -> str:
    """CIK number search and rerieval for given ticker.

    Args:
        ticker (str): Company ticker symbol
        cik_data (dict): SEC CIK data (whole file)

    Returns:
        str: string of company CIK numbers

    Raises:
        InvalidArgumentError: If CIK number not found
    """
    ticker_lower = ticker.lower().strip()
    for entry in cik_data.values():
        if entry.get('ticker', '').lower() == ticker_lower:
            cik = str(entry.get('cik_str')).zfill(10)
            logger.debug(f'{ticker.upper()} CIK #: {cik}')
            return cik

    logger.error(f'CIK not found for {ticker.upper()}')
    raise InvalidArgumentError(f"CIK not found for {ticker.upper()}")

def get_facts_request(ticker: str) -> dict:
    """Fetch facts from SEC servers.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: Facts for given ticker
    """
    ticker = ticker.lower().strip()
    headers = {'User-Agent': cfg.edgar_user_agent()}

    logger.debug(f"EDGAR API: Fetching CIK data for: {ticker.upper()}")
    cik_data = safe_status_get(cfg.EDGAR_CIK_URL, headers=headers)
    cik = _find_cik(ticker, cik_data)
    facts_url = f"{cfg.EDGAR_FACTS_URL}{cik}.json"

    logger.debug(f"EDGAR API: Fetching facts for: {ticker.upper()}")
    time.sleep(1) # be polite to SEC server
    return safe_status_get(facts_url, headers=headers)

def _load_json(path: Path, data_type: str) -> dict:
    """Load JSON file with error handling.

    Args:
        path (Path): Path to JSON file
        data_type (str): Description for error messages

    Returns:
        dict: containing target JSON data

    Raises:
        DataError: if filing is missing, corrupted, or fails to load
    """
    if not path.exists():
        logger.error(f'{data_type} file missing: {path}')
        raise DataError(f'{data_type} file not found')

    try:
        with open(path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as err:
        logger.error(f'Corrupted {data_type} file: {path}')
        raise DataError(f'Corrupted {data_type} file') from err
    except Exception as err:
        logger.exception(f'Failed to load {data_type} file: {path}')
        raise DataError(f'Failed to load {data_type} file') from err

def get_facts_bulk(ticker: str) -> dict:
    """Fetch facts from bulk download.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: Facts for given ticker

    Raise:
        DataError: If nothing found
    """
    ticker = ticker.lower().strip()
    bulk_dir = cfg.BULK_DIR

    cik_path = bulk_dir / 'company_tickers.json'
    cik_data = _load_json(cik_path, 'CIK mapping')
    cik = _find_cik(ticker, cik_data)

    facts_path = bulk_dir / 'companyfacts' / f"CIK{cik}.json"
    facts = _load_json(facts_path, f'CIK: {cik} facts')
    logger.debug(f"EDGAR data found for {ticker.upper()}")
    return facts

