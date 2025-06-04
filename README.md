# qemy (prototype): command-line financial data engine for researchers and traders

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)

qemy is a prototype financial data engine designed for market and economic analysis. It aims to simplify and automate research by providing SEC filings, stock market data, macroeconomic indicators, and the tools needed to analyze and visualize them — all within a convenient CLI. This repository contains the core data pipeline and command-line interface.

**Work in Progress**

qemy is in early development. I'm building this as a personal tool first, and refining as I go.
Features may change, break, or get replaced as the project evolves.

Suggestions are welcome!

- [Start a Discussion](https://github.com/ryan-rashidian/qemy/discussions/new/choose)
- [Report a Bug / Open an Issue](https://github.com/ryan-rashidian/qemy/issues/new)

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Setup API Keys](#setup-api-keys)
- [Optional: Setup Launch Script](#optional-setup-launch-script)
- [Usage](#usage)
- [Development Notes](#development-notes)
- [Legal / Attribution](#legal--attribution)
- [License](#license)

---

## Features

- CLI: Command line interface entry point.
- Fetch: stock market data from Tiingo API.
- Fetch: or download SEC filing data (e.g. 10K/10Q) from SEC EDGAR API.
- Fetch: economic data from FRED API
- Chart: price history, linear regression, etc.
- (In Progress) Model: DCF, Comps, and other valuation models.
- (Planned) Filter: metric based stock screening.
- (Planned) Backtest: Monte Carlo and historical simulations.
- (Planned) Profile: user accounts and portfolio tracking.

Note: Filing data is limited to US markets (GAAP) and all metrics are in USD for now. Support for global markets (IFRS) and currency conversion is planned. 

---

## Installation 

### Clone the repo:

```bash
git clone https://github.com/ryan-rashidian/qemy.git
```

### Install qemy with dependencies:

It's recommended to use a Python venv or Conda.

#### Option 1 (recommended): 

```bash
pip install .
```

#### Option 2 (for devs):

```bash
pip install -r requirements.txt # or requirements-dev.txt
```

---

## Setup API Keys

API keys available free of charge. Sign up required for Tiingo API and Fred API:

- https://fred.stlouisfed.org/docs/api/fred/
- https://www.tiingo.com/
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces (No sign up or API key required for EDGAR API. Users will be prompted for a "User Agent" during the setup wizard.)

Run the CLI and qemy will guide you through an API key setup wizard on first launch.

- Refer to "Usage" below for info related to API usage and data limitations.

Or manually create a .env file in project root directory and add API keys like this:

```env
TIINGO_API_KEY=<your_key_here>
FRED_API_KEY=<your_key_here>
EDGAR_USER_AGENT=<your user agent> # EDGAR_USER_AGENT=john johndoe@example.com
```

Make sure .env is included in .gitignore to keep your keys secure.

IMPORTANT: Read "Legal / Attribution" before using qemy with any 3rd party API service.

---

## Optional: Setup Launch Script

- Recommended for convenience if you are working with the source code directly, and took option 2 during the installation.

### Set path to your venv in the bash script

In the scripts directory, find the qemy bash script and open with a text editor:

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

Also from scripts directory:

```bash
chmod +x qemy
```

### Create Path in .bashrc

```bash
nano ~/.bashrc
```

Add the following to the bottom of your .bashrc. Replace "path/to/your/project/root/scripts" with your own: 

```bash
# PATH for Qemy
export PATH="$HOME/path/to/your/project/root/scripts:$PATH"
```

---

## Usage

### Launch CLI

To start the qemy command-line interface run:

```bash
qemy
```

from any terminal or shell.

If you setup the optional launch script, you can also run: 

```bash
qemy
```

from any bash terminal or shell.

Alternatively, run the CLI manually with:

```bash
source ~/path/to/qemyenv/bin/activate
# Conda users: change above line to "conda activate qemyenv"
cd ~/path/to/qemy # path to project root directory
python -m qemy.cli
```

### Use CLI

```bash
qemy> help
qemy> help filing
qemy> filing AAPL
qemy> chart_lr TSLA -p 5y
qemy> exit
```

Proper documentation is being planned. For now, refer to the help commands for more information.

- This program does not require paying any fees or subscriptions. There are paid subscriptions for Tiingo API available in order to increase data usage limitation. Be mindful data usage/request limits for all APIs. More info and tracking is available on their websites.

---

## Development Notes

Known Issues:

- (Non-critical) Parsing logic in SEC_Filings class is slightly inaccurate. Filing data is not always in chronological order. The issue has been solved in testing, and a fix will be implemented soon. 
- (Non-critical) DCF model is not yet factoring a company's net debt metric into the calculation. Waiting for implementation of better parsing logic, referenced in the previous issue. 

Ideas:

- Backtesting engine for Monte Carlo and historical simulations.
- Stock screening and filtering.
- IFRS filing support in SEC_Filings parser and currency conversion. 
- "Modes" - or sub-sections within the CLI for plots, models, etc. 
- (In Progress) Guide's and helpful information included in CLI.
- (In Progress) Valuation modeling using DCF, comps, etc.

Note (2025-06-03):

- This is my first serious project on GitHub. Earlier commits show my learning curve with git, and workflow habits. Since then, I've been refining my process. - Thanks for understanding.

---

## Legal / Attribution

By using the qemy application, you agree to the qemy Terms of Use ("Legal / Attribution") below and Licensing terms.

- Users are responsible for complying with the terms of any third-party APIs used.
- qemy is not affiliated with the SEC or Federal Reserve.
- qemy does not collect or transmit any user data, personal information, or API usage statistics.
- Data may have errors, delays, or be incomplete.
- 3rd party APIs sign ups must be done through their respective websites. qemy does not include a automated sign up process for 3rd party APIs.

### SEC EDGAR

- This product uses the SEC EDGAR API but is not endorsed or certified by the U.S. Securities and Exchange Commission.

### Fred API

- This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.

### Tiingo API

- This software integrates with the Tiingo API for stock market data, but does not cache data or redistribute data, API keys or any user data (such as tracking endpoint usage).
- This software is not owned, managed by, or affiliated with/by Tiingo.

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

