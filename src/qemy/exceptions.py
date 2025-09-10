"""Custom exceptions for Qemy."""

class ClientRequestError(Exception):
    """Raised when a client request fails or encounters an error."""
    pass

class MissingCredentialError(Exception):
    """Raised when a required API credential is missing."""
    pass

