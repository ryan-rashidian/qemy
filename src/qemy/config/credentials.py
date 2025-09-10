"""API credentials and authentication for Qemy."""

import os
from dotenv import load_dotenv, set_key

from qemy.exceptions import MissingCredentialError
from qemy.config.paths import DOTENV_PATH

if not DOTENV_PATH.exists():
    DOTENV_PATH.touch()

load_dotenv(dotenv_path=DOTENV_PATH)

def write_credential(env_var: str, value: str) -> None:
    """Write user-credentials to the .env file."""
    set_key(DOTENV_PATH, env_var, value)

def require_credential(service: str, env_var: str) -> str:
    """Require user-credentials for access."""
    value = os.getenv(env_var)
    if not value:
        raise MissingCredentialError(
            f'{service} API credentials are not configured.'
        )
    return value

