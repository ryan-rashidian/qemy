"""Common tools and utilities for /data/ package."""

import logging
from datetime import datetime
from pathlib import Path

import requests
from dateutil.relativedelta import relativedelta

from qemy.exceptions import APIClientError

logger = logging.getLogger(__name__)

def parse_period(period_str) -> tuple[str, str]:
    """Convert shorthand period into formatted date-time strings.

    Args:
        period_str (str): Shorthand period string (e.g., "2W", "4M")

    Returns:
        tuple[str, str]: Tuple of start and end date strings

    Raises:
        ClientError: If invalid units
    """
    now = datetime.now()

    try:
        unit = period_str[-1].upper()
        value = int(period_str[:-1])

        match unit:
            case 'D':
                start_date = now - relativedelta(days=value)
            case 'W':
                start_date = now - relativedelta(weeks=value)
            case 'M':
                start_date = now - relativedelta(months=value)
            case 'Y':
                start_date = now - relativedelta(years=value)
            case _:
                raise APIClientError("Invalid unit")

        return start_date.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d')

    except ValueError as e:
        raise APIClientError(
            "Invalid period format.\n"
            "Use: D, W, M, or Y\n"
            "Usage: <INTEGER><UNITS>\n"
            "Example: '6M', '2Y', '5D'"
        ) from e

def safe_status_get(
    url: str,
    headers: dict[str, str] | None=None,
    params: dict[str, str] | None=None
) -> dict:
    """Request with error handling.

    Args:
        url (str): Request URL
        headers (dict[str, str]): Request headers
        params (dict[str, str]): Request parameters

    Returns:
        dict: Response data in dictionary format

    Raises:
        ClientError: If request fails
    """
    response = None
    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error:\n{e}")
        raise APIClientError("HTTP Error") from e

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed:\n{e}")
        raise APIClientError("Request failed") from e

    except Exception as e:
        logger.exception(f"Error:\n{e}")
        raise APIClientError("Unexpected Error") from e

def safe_status_download(
    url: str,
    headers: dict[str, str] | None=None,
    dest_path: Path | None=None
):
    """Request download with error handling.

    Args:
        url (str): Request URL
        headers (dict[str, str]): Request headers
        dest_path (Path): Download directory path

    Raises:
        ClientError: If download fails
    """
    if not isinstance(dest_path, Path):
        logger.error("Incorrect type for: dest_path")
        raise APIClientError("Incorrect type for: dest_path")

    try:
        with requests.get(url=url, headers=headers, stream=True) as r:
            r.raise_for_status()
            if isinstance(dest_path, Path):
                with open(dest_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error during download:\n{e}")
        raise APIClientError("HTTP Error") from e

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed:\n{e}")
        raise APIClientError("Request failed") from e

    except Exception as e:
        logger.exception(f"Error:\n{e}")
        raise APIClientError("Unexpected Error") from e

