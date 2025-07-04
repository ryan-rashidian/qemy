"""Get companyfacts from SEC servers and bulk download.

This module contains get_ functions that return facts through different means.
"""

import logging
import time
import json

from qemy import _config as cfg
from qemy.utils.safe_request import safe_status_get

logger = logging.getLogger(__name__)

def _find_cik(ticker: str, cik_data: dict) -> str | None:
    """CIK # search and rerieval for given ticker.

    Args:
        ticker (str): Company ticker symbol
        cik_data (dict): All SEC CIK data

    Returns:
        str: string of company CIK #
        None: failed to find ticker in cik_data
    """
    cik = None
    for entry in cik_data.values():
        if entry.get('ticker', '').lower() == ticker:
            cik = str(entry.get('cik_str')).zfill(10)
            break
    return cik

def get_facts_request(ticker: str) -> dict | None:
    """Fetch facts from SEC servers.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: facts for given ticker
        None: failed to find facts for given ticker
    """
    ticker = ticker.lower().strip()
    headers = {'User-Agent': cfg.edgar_user_agent()} 

    cik_data = safe_status_get(cfg.EDGAR_CIK_URL, headers=headers)
    if not cik_data:
        logger.warning("Failed to fetch CIK data from SEC servers.")
        return None

    cik = _find_cik(ticker, cik_data)
    if cik is None:
        logger.warning(f"CIK not found for ticker: {ticker.upper()}")
        return None

    logger.info(f"Fetching facts from SEC for: {ticker.upper()}")
    time.sleep(1) # Be polite to SEC server

    facts_url = f"{cfg.EDGAR_FACTS_URL}{cik}.json"
    facts = safe_status_get(facts_url, headers=headers)

    if not facts:
        logger.warning(f"Failed to fetch facts from SEC servers for {cik}")

    logger.info(f"EDGAR data found for {ticker.upper()}")
    return facts

def get_facts_bulk(ticker: str) -> dict | None:
    """Fetch facts from bulk download.

    Args:
        ticker (str): Company ticker symbol

    Returns:
        dict: facts for given ticker
        None: failed to find facts for given ticker
    """
    ticker = ticker.lower().strip()
    bulk_dir = cfg.BULK_DIR

    try:
        with open(bulk_dir / 'company_tickers.json', 'r') as f:
            cik_data = json.load(f)
    except FileNotFoundError:
        logger.warning(f"CIK not found in {bulk_dir}")
        return None

    cik = _find_cik(ticker, cik_data)
    if cik is None:
        logger.warning(f"CIK not found for ticker: {ticker.upper()}")
        return None

    facts_path = bulk_dir / 'companyfacts' / f"CIK{cik}.json"
    if not facts_path.exists():
        logger.warning(f"Facts file missing: {facts_path}")
        return None

    try:
        with open(facts_path, 'r') as f:
            facts = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Corrupted JSON file for {cik}\n{e}")
        return None
    except Exception as e:
        logger.exception(f"Failed to load facts JSON for {cik}\n{e}")
        return None

    logger.info(f"EDGAR data found for {ticker.upper()}")
    return facts

