"""Tools for Qemy plugins."""

import logging


class BasePlugin:
    """Base class for Qemy plugins."""
    name = "BasePlugin"
    description = "Base class for Qemy plugins"
    version = "0.1.1"

    def __init__(
        self,
        ticker: str,
        period: str,
        num: int,
        **kwargs: str
    ):
        """Initialize CLI commands as inherited variables.

        Args:
            ticker (str): -t --ticker in CLI
            period (str): -p --period in CLI
            num (int): -n --num in CLI
            **kwargs (str): Custom CLI args for plugins
        """
        self.ticker = ticker
        self.period = period
        self.num = num
        self.args = kwargs
        self.logger = logging.getLogger(self.name)

    def run(self) -> dict:
        """Called by the CLI in order to print plugin output.

        Returns:
            dict: Expected return type in the CLI
        """
        raise NotImplementedError("Plugin must use run() method")

    def help(self):
        """CLI -h --help info for plugins."""
        return f"{self.name} - {self.description}\nNo help found"

    def log(self, message: str, level: int=logging.INFO):
        """Print logging for plugins.

        Args:
            message (str): log string
        """
        self.logger.log(level, message)

