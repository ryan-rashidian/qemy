"""Custom exceptions for Qemy."""

class QemyError(Exception):
    """Base class for all Qemy errors."""
    pass

class ClientDataError(QemyError):
    """Raised when a client fails to read data."""
    pass

class ClientParsingError(QemyError):
    """Raised when a client fails to parse data."""
    pass

class ClientRequestError(QemyError):
    """Raised when a client request fails or encounters an error."""
    pass

class DownloadError(QemyError):
    """Raised when an attempted download fails."""
    pass

class InvalidArgumentError(QemyError):
    """Raised when an invalid argument is passed."""
    pass

class InvalidSyntaxError(QemyError):
    """Raised when invalid syntax is used in a string."""
    pass

class JSONDecodingError(QemyError):
    """Raised when a JSON file cannot be properly decoded or validated."""
    pass

class MissingCredentialError(QemyError):
    """Raised when a required API credential is missing."""
    pass

class AnalyticsMetricError(QemyError):
    """Raised when a metric calculation fails."""
    pass

class AnalyticsModelError(QemyError):
    """Raised when a model calculation fails."""
    pass

