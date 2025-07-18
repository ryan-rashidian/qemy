"""Custom exceptions for Qemy."""

class QemyError(Exception):
    """Base exception for Qemy errors."""
    pass

class APIClientError(QemyError):
    """Raised for errors in API clients."""
    pass

class DataError(QemyError):
    """Raised for data related errors."""
    pass

class ParseError(QemyError):
    """Raised for parsing errors."""
    pass

class MetricError(QemyError):
    """Raised for metric related errors."""
    pass

class ModelError(QemyError):
    """Raised for model related errors."""
    pass

class InvalidArgumentError(QemyError):
    """Raised when invalid argument is given."""
    pass
