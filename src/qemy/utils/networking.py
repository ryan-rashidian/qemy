"""Networking utilities for Qemy."""

import requests

from qemy.exceptions import ClientRequestError

def make_request(
    url: str,
    headers: dict[str, str] | None = None,
    params: dict[str, str] | None = None
) -> dict:
    """Make a request wrapped with error handling.

    Args:
        url (str): request URL
        headers (str): request headers
        params (str): request parameters

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
        return response.json()

    except requests.exceptions.HTTPError as e:
        raise ClientRequestError('HTTP Error') from e
    except requests.exceptions.RequestException as e:
        raise ClientRequestError('Request Error') from e
    except Exception as e:
        raise ClientRequestError('Unexpected request Error') from e

def download_data():
    pass

