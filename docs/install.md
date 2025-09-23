# Development Installation

```bash
pip install -e .
# or
pip install -r requirements-dev.txt
```

## Optional - Manually Create .env

From the project root, create a ".env" file and add API keys like this:

```env
TIINGO_API_KEY='<your_key_here>'
FRED_API_KEY='<your_key_here>'
EDGAR_USER_AGENT='<your user agent>' # EDGAR_USER_AGENT='john johndoe@example.com'
```

For developers: Make sure .env is included in .gitignore to keep your keys secure.

