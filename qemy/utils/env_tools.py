"""Functions relating to os.getenv environment variables."""

import os
import sys

def get_env_str(key: str) -> str:
    """Ensure string is returned from os.getenv
    
    Args:
        key (str): Name of environment variable (e.g., "EDGAR_USER_AGENT")

    Returns:
        str: Credential information for APIs corresponding to the key arg
    """
    val = os.getenv(key) # Returns: str | None

    if val is None:
        print(f"Missing API key: {key}")
        print(f"Exiting Qemy, Please setup API keys correctly.")
        sys.exit(1)

    return val

