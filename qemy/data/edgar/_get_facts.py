"""Get companyfacts from SEC servers and bulk download.

This module contains get_ functions that return company facts.
"""

import json
import logging
import time

from qemy import _config as cfg
from qemy.data._api_tools import safe_status_get
from qemy.exceptions import DataError, InvalidArgumentError

logger = logging.getLogger(__name__)

def _find_cik(ticker: str, cik_data: dict) -> str:
    """CIK # search and rerieval for given ticker.

    Args:
        ticker (str): Company ticker symbol
        cik_data (dict): All SEC CIK data

    Returns:
        str: string of company CIK #

    Raises:
        InvalidArgumentError: If CIK not found
    """
    cik = None
    for entry in cik_data.values():
        if entry.get('ticker', '').lower() == ticker:
            cik = str(entry.get('cik_str')).zfill(10)
            break
    if cik is not None:
        return cik
    else:
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

    logger.debug(f"Fetching cik data for: {ticker.upper()}")
    cik_data = safe_status_get(cfg.EDGAR_CIK_URL, headers=headers)
    cik = _find_cik(ticker, cik_data)
    facts_url = f"{cfg.EDGAR_FACTS_URL}{cik}.json"

    logger.debug(f"Fetching facts from SEC for: {ticker.upper()}")
    time.sleep(1) # Be polite to SEC server

    return safe_status_get(facts_url, headers=headers)

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

    try:
        with open(bulk_dir / 'company_tickers.json', 'r') as f:
            cik_data = json.load(f)

    except FileNotFoundError as err:
        logger.error(f"CIK not found in {bulk_dir}")
        raise DataError("CIK not found") from err

    cik = _find_cik(ticker, cik_data)
    facts_path = bulk_dir / 'companyfacts' / f"CIK{cik}.json"
    if not facts_path.exists():
        logger.warning(f"Facts file missing: {facts_path}")
        raise DataError("Facts file not found")

    try:
        with open(facts_path, 'r') as f:
            facts = json.load(f)

    except json.JSONDecodeError as err:
        logger.error(f"Corrupted JSON file for {cik}\n{err}")
        raise DataError("Corrupted JSON file") from err
    except Exception as err:
        logger.exception(f"Failed to load facts for {cik}\n{err}")
        raise DataError("Failed to load facts") from err

    logger.debug(f"EDGAR data found for {ticker.upper()}")
    return facts

