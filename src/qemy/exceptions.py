"""Custom exceptions for Qemy."""

class QemyError(Exception):
    """Base class for all Qemy errors."""
    pass

class ClientRequestError(QemyError):
    """Raised when a client request fails or encounters an error."""
    pass

class DownloadError(QemyError):
    """Raised when an attempted download fails."""
    pass

class InvalidSyntaxError(QemyError):
    """Raised when invalid syntax is used in a string."""
    pass

class MissingCredentialError(QemyError):
    """Raised when a required API credential is missing."""
    pass

