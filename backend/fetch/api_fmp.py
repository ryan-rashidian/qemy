import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv('FMP_API_KEY')
BASE_URL = 'https://financialmodelingprep.com/api/v3'

def get_dcf(ticker):
    url = f"{BASE_URL}/discounted-cash-flow/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0]

def get_profile(ticker):
    url = f"{BASE_URL}/profile/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0]

def get_ratios(ticker):
    url = f"{BASE_URL}/ratios-ttm/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0]

def get_balance(ticker):
    url = f"{BASE_URL}/balance-sheet-statement/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0]

def get_beta(ticker):
    url = f"{BASE_URL}/beta/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0]

def get_metrics(ticker):
    url = f"{BASE_URL}/key-metrics/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0]

def get_52_week(ticker):
    url = f"{BASE_URL}/stock/52-week-high-low/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0]

def get_ev(ticker):
    url = f"{BASE_URL}/enterprise-values/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0]

def get_income(ticker):
    url = f"{BASE_URL}/income-statement/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0]

def get_cf(ticker):
    url = f"{BASE_URL}/cash-flow-statement/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0]
