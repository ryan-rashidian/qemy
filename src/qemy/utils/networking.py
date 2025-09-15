"""Networking utilities for Qemy."""

import requests
from pathlib import Path

from qemy.exceptions import ClientRequestError, DownloadError
from qemy.config.logger import get_logger

logger = get_logger(__name__)

def make_request(
    url: str,
    headers: dict[str, str] | None = None,
    params: dict[str, str] | None = None
) -> dict:
    """Make a request wrapped with error handling.

    Args:
        url (str): request URL
        headers (dict[str, str]): request headers
        params (dict[str, str]): request parameters

    Returns:
        dict: dictionary of requested data

    Raises:
        ClientRequestError: if request fails

    Note:
        `requests.get` accepts None for `headers` and `params`,
        which means they are ignored if not provided.
    """
    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        logger.debug(f'Request complete: {url}')
        return response.json()

    except requests.exceptions.HTTPError as e:
        logger.error('HTTP Error')
        raise ClientRequestError('HTTP Error') from e

    except requests.exceptions.RequestException as e:
        logger.error('Request Error')
        raise ClientRequestError('Request Error') from e

    except Exception as e:
        logger.error('Unexpected request Error')
        raise ClientRequestError('Unexpected request Error') from e

def download_data(
    url: str,
    dest_path: Path,
    headers: dict[str, str] | None = None
) -> None:
    """File downloader wrapped with error handling.

    Args:
        url (str): request URL
        headers (dict[str, str]): request headers
        dest_path (pathlib.Path): download path destination

    Raises:
        DownloadError: if attempted download fails
    """
    try:
        with requests.get(url=url, headers=headers, stream=True) as r:
            r.raise_for_status()
            logger.debug(f'Request complete: {url}')
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f'Download complete: {dest_path.resolve()}')

    except requests.exceptions.HTTPError as e:
        logger.error('HTTP Error')
        raise DownloadError('HTTP Error') from e

    except requests.exceptions.RequestException as e:
        logger.error('Request Error')
        raise DownloadError('Request Error') from e

    except Exception as e:
        logger.error('Unexpected request Error')
        raise DownloadError('Unexpected request Error') from e

