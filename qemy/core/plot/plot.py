from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from qemy.utils.filetools import get_next_path
from qemy.data.api_tiingo import StockMarket
from qemy.data import api_fred as fred

project_root = Path(__file__).resolve().parents[3]
export_dir = project_root / "exports" / "charts"
export_dir.mkdir(parents=True, exist_ok=True)

def plot_models(ticker, title='title', save=False, plot_func=None):
    plt.figure(figsize=(14, 8))
    if plot_func:
        plot_func()

    plt.title(f"{title} for {ticker}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.tight_layout()

    if save == True:
        output_path =  get_next_path(export_dir, name='modelchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_price(ticker, period):
    data = StockMarket().get_prices(ticker=ticker, period=period)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])

    plt.figure(figsize=(14, 8))
    plt.plot(df['date'], df['close'], label='Price', color='green', linewidth=3, marker= 'o', alpha=0.8)
    if len(df['date']) >= 250:
        df['50_DMA'] = df['close'].rolling(window=50).mean()
        df['200_DMA'] = df['close'].rolling(window=200).mean()
        plt.plot(df['date'], df['50_DMA'], label='50 DMA', color='blue', linewidth=1, alpha=0.5)
        plt.plot(df['date'], df['200_DMA'], label='200 DMA', color='red', linewidth=2, alpha=0.5)
    plt.xlabel('Date')
    plt.ylabel('Price (Log-Scale)')
    plt.yscale('log')
    plt.title('Log-Scaled Daily Closing Prices')
    plt.grid(True, which='both')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_cpi(period, save=False, units='pc1'):
    data = fred.get_cpi_inflation(period=period, units=units)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='CPI Inflation', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Inflation')
    plt.title(f"CPI Inflation: {units}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='cpichart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()
    
def plot_gdp(period, save=False, units='pc1'):
    data = fred.get_gdp(period=period, units=units)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='GDP', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('GDP')
    plt.title(f"GDP: {units}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='gdpchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_sentiment(period, save=False, units='pch'):
    data = fred.get_sentiment(period=period, units=units)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='Sentiment', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Sentiment')
    plt.title(f"Sentiment: {units}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='sentchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_nfp(period, save=False, units='pc1'):
    data = fred.get_nf_payrolls(period=period, units=units)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='NFP', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('NFP')
    plt.title(f"Non-Farm Payrolls: {units}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='nfpchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_interest(period, save=False, units='pc1'):
    data = fred.get_interest(period=period, units=units)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='interest', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Interest')
    plt.title(f"Interest: {units}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='interestchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_jobc(period, save=False, units='pc1'):
    data = fred.get_jobless_claims(period=period, units=units)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='jobless claims', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Jobless Claims')
    plt.title(f"Jobless Claims: {units}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='jobcchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_unemployment(period, save=False, units='pc1'):
    data = fred.get_unemployment(period=period, units=units)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='unemployment', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Unemployment rate')
    plt.title(f"Unemployment rate: {units}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='unemchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_ind_prod(period, save=False, units='pc1'):
    data = fred.get_ind_prod(period=period, units=units)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='ind prod', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Ind Prod')
    plt.title(f"Industrial Production: {units}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='indpchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

def plot_netex(period, save=False, units='lin'):
    data = fred.get_netex(period=period, units=units)
    df = pd.DataFrame(data)

    plt.figure(figsize=(14, 8))
    plt.plot(df.index, df['value'], label='NetEx', color='green', linewidth=3, marker= 'o', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('NetEx')
    plt.title(f"Real Net Exports of Goods and Services: {units}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save == True:
        output_path =  get_next_path(export_dir, name='netexchart', ext='png')
        plt.savefig(output_path)
        plt.show()
    else:
        plt.show()

