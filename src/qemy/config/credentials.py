"""API credentials and authentication for Qemy."""

import os
from typing import Optional, Tuple

from dotenv import load_dotenv, set_key, unset_key

from qemy.config.paths import DOTENV_PATH
from qemy.exceptions import MissingCredentialError

if not DOTENV_PATH.exists():
    DOTENV_PATH.touch()

load_dotenv(dotenv_path=DOTENV_PATH)

def write_credential(env_var: str, value: str) -> None:
    """Write user-credentials to the .env file."""
    set_key(DOTENV_PATH, env_var, value)

def remove_credential(env_var: str) -> Tuple[Optional[bool], str]:
    """Remove user-credentials from the .env file."""
    return unset_key(DOTENV_PATH, env_var)

def require_credential(service: str, env_var: str) -> str:
    """Require user-credentials for access."""
    value = os.getenv(env_var)
    if not value:
        raise MissingCredentialError(
            f'{service} API credentials are not configured.'
        )
    return value

