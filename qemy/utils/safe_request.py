import logging
from pathlib import Path
import requests

logger = logging.getLogger(__name__)

def safe_status_get(url, headers=None, params=None):
    response = None
    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTPError: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed:\n{e}")
    except Exception as e:
        logger.exception(f"Error: {e}")
    return None

def safe_status_download(url, headers=None, dest_path=None):
    if not isinstance(dest_path, Path):
        logger.error("Download failed: dest_path must be valid Path object")
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
        logger.error(f"HTTPError: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    except Exception as e:
        logger.exception(f"Error: {e}")
    return False

