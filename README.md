# Qemy Prototype: Financial Data Engine 

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)

Qemy is a prototype financial data engine designed for stock market analysis and research. This repo contains the core data pipeline.

---

## Features (* = in progress) (** = planned)

- Fetches stock data from APIs
- Command line interface
- Easy integration with financial models or frontends
- *Charts and Graphs
- **Stock screening/filtering with score based ranking
- **User profiles and portfolio tracking
- **Backtesting and indicators for quant trading strategies

---

## Installation 

### Clone the repo:

```bash
git clone https://github.com/ryan-rashidian/qemy.git
```
### Install dependencies:

#### Option 1: Using Python venv:

```bash
cd qemy # or which-ever folder you keep venvs in
python -m venv qemyenv
source qemyenv/bin/activate # for Linux/MacOS
# or
venv\Scripts\activate # for Windows
# then
pip install -r requirements.txt
```

#### Option 2: Using Conda:

```bash
conda create --name qemyenv python=3.11.2
conda activate qemyenv
pip install -r requirements.txt
```

---

## Setup API keys

API keys available with free plans. Sign up required for both Tiingo and FMP:

- https://financialmodelingprep.com/
- https://www.tiingo.com/

IMPORTANT: Read "Usage" below for info related to API usage and data limitations.
API logic is restricted to respective modules (api_tiingo.py, api_fmp.py), and wrapped in various functions. To replace with alternative data source, simply rewrite those functions while being mindful to keep naming consistent.

Create a .env file in qemy root directory and add API keys like this:
```env
TIINGO_API_KEY=your_key_here
FMP_API_KEY=your_key_here
```
Make sure .env is included in .gitignore to keep your keys secure.

---

## Optional: Setup launch script

### Set path to your venv in the bash script

From the project root directory find the qemy bash script and open it in a text editor:

```bash
#!/bin/bash

orig_dir=$(pwd)
source ~/path/to/qemyenv/bin/activate # make sure this matches your venv activate path
# Conda users: change above line to "conda activate qemyenv"
cd ~/path/to/qemy # change to your project root directory
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
Tip: $HOME is a bash environment variable that refers to your home directory (regardless of its unique name).

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
- Users are responsible for complying with the terms of any third-party APIs used.
- This program does not require paying any fees or subscriptions. Paid versions of FMP and Tiingo APIs are optionally available in order to increase data usage limitation. Be mindful of Tiingo API and FMP API data usage limits. More info and tracking is available on their websites.

---

## Development Notes

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
