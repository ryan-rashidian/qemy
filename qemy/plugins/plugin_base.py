"""Module for plugin classes."""

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
            ticker (str):
            period (str):
            num (int):
            **kwargs (str):
        """
        self.ticker = ticker
        self.period = period
        self.num = num
        self.args = kwargs

    def run(self):
        raise NotImplementedError("Plugin must use run() method")

    def help(self):
        """CLI -h --help info for plugins."""
        return f"{self.name} - {self.description}\nNo help found"

    def log(self, message):
        """Print logging for plugins.

        Args:
            message (str): log string
        """
        print(f"[{self.name}] {message}")
        
