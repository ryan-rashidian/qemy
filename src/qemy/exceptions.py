"""Custom exceptions for Qemy."""

class ClientRequestError(Exception):
    """Raised when a client request fails or encounters an error."""
    pass

class InvalidSyntaxError(Exception):
    """Raised when invalid syntax is used in a string."""
    pass

class MissingCredentialError(Exception):
    """Raised when a required API credential is missing."""
    pass

