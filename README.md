# Qemy (Prototype): Financial Data Engine 

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)

Qemy is a prototype financial data engine designed for market/economic analysis and research. This repository contains the core data pipeline.

---

## Features (* = in progress) (** = planned)

- CLI: Command line interface entry point.
- Fetch: stock market data from Tiingo API.
- *Fetch: economic data from FRED API
- *Fetch: SEC filing data (e.g. 10K/10Q) from SEC EDGAR API.
- *Charting: price history, linear regression, etc.
- *Session: persisting work environments.
- **Filter: metric based stock screening.
- **Profile: user accounts and portfolio tracking.
- **Backtest: Monte Carlo and historical simulations.
- **Cache: SQLite local cache for SEC filings.

---

## Installation 

### Clone the repo:

```bash
git clone https://github.com/ryan-rashidian/qemy.git
```

### Install dependencies:

#### Option 1: Using Python venv:

```bash
cd path/to/your/venvs 
python -m venv qemyenv
source qemyenv/bin/activate # for Linux/MacOS
# or
qemyenv\Scripts\activate # for Windows
# then
pip install -r requirements.txt
```

#### Option 2: Using Conda:

```bash
conda create --name qemyenv python=3.12.3
conda activate qemyenv
pip install -r requirements.txt
```

---

## Setup API Keys

API keys available free of charge. Sign up required for Tiingo API and Fred API:

- https://fred.stlouisfed.org/docs/api/fred/
- https://www.tiingo.com/
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces (No sign up or API key required for EDGAR API. Users will be prompted for a "User Agent" during the setup wizard.)

IMPORTANT: Read "Legal / Attribution" before using Qemy with any 3rd party API service.

- Refer to "Usage" below for info related to API usage and data limitations.

API key setup wizard included. Run the CLI to receive a prompt.

Or manually create a .env file in project root directory and add API keys like this:

```env
TIINGO_API_KEY=<your_key_here>
FRED_API_KEY=<your_key_here>
EDGAR_USER_AGENT=<your user agent> # EDGAR_USER_AGENT=john johndoe@example.com
```

Make sure .env is included in .gitignore to keep your keys secure.

---

## Optional: Setup Launch Script

- Recommended for convenience if you are working with the source code directly.

### Set path to your venv in the bash script

From the project root directory, find the qemy bash script and open with a text editor:

```bash
#!/bin/bash

orig_dir=$(pwd)
source ~/path/to/qemyenv/bin/activate # make sure this matches your venv activate path
# Conda users: change above line to "conda activate qemyenv"
cd ~/path/to/qemy # match with your project root directory
python -m frontend.cli
deactivate 
# Conda users: change above line to "conda deactivate"
cd "$orig_dir"
```

### Turn qemy script into an executable

Also from project root directory:

```bash
chmod +x qemy
```

### Create Path in .bashrc

```bash
nano ~/.bashrc
```

Add the following to the bottom of your .bashrc. Replace "path/to/your/project/root" with your own: 

```bash
# PATH for Qemy
export PATH="$HOME/path/to/your/project/root:$PATH"
```

---

## Usage

- If you setup the optional launch script, you can simply run: 

```bash
qemy
```

from any bash terminal session.

- Alternatively, run the CLI manually with:

```bash
source ~/path/to/qemyenv/bin/activate
# Conda users: change above line to "conda activate qemyenv"
cd ~/path/to/qemy # path to project root directory
python -m frontend.cli
```

- This program does not require paying any fees or subscriptions. There are paid subscriptions for Tiingo API available in order to increase data usage limitation. Be mindful data usage/request limits for all APIs. More info and tracking is available on their websites.

---

## Legal / Attribution

By using the Qemy application, you agree to the Qemy Terms of Use ("Legal / Attribution") below and Licensing terms.

- Users are responsible for complying with the terms of any third-party APIs used.
- Qemy is not affiliated with the SEC or Federal Reserve.
- Data may have errors, delays, or be incomplete.
- 3rd party APIs sign ups must be done through their respective websites. Qemy does not, and will not ever include a automated sign up process for 3rd party APIs.

### SEC EDGAR

- This product uses the SEC EDGAR API but is not endorsed or certified by the U.S. Securities and Exchange Commission.

### Fred API

- This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.

### Tiingo API

- This software integrates with the Tiingo API for stock market data, but does not cache data or redistribute data, API keys or any user data (such as tracking endpoint usage).
- This software is not owned, managed by, or affiliated with/by Tiingo.

---

## Development Notes

// Dev notes will go here in future versions

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

