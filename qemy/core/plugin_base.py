
class BasePlugin:
    name = "BasePlugin"
    description = "Base class for Qemy plugins"
    version = "0.1.0"

    def __init__(self, ticker, period, num, **kwargs):
        self.ticker = ticker
        self.period = period
        self.num = num
        self.args = kwargs

    def run(self):
        raise NotImplementedError("Plugin must use run() method")

    def help(self):
        return f"{self.name} - {self.description}\nNo help found"

    def log(self, message):
        print(f"[{self.name}] {message}")
        
