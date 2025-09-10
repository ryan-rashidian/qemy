"""EDGARClient module."""

class EDGARClient:
    """Main Client for EDGAR API."""

    def __init__(self, ticker: str):
        """Initialize data pipeline for client."""
        self.ticker = ticker.strip().upper()
        
