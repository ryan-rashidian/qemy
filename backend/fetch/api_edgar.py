import os
import time
import json
from math import nan
import pandas as pd
from pathlib import Path
from . import api_edgar_lists as keylist
from .utils_fetch import safe_status_get

class SEC_Filings:
    def __init__(self, ticker, use_requests=False):
        self.HEADERS = {'User-Agent': os.getenv('EDGAR_USER_AGENT')} 
        self.ticker = ticker.upper().strip()
        self.cik = None
        self.facts = None
        try:
            if use_requests:
                url = 'https://www.sec.gov/files/company_tickers.json'
                data = safe_status_get(url=url, headers=self.HEADERS)
                if data:
                    for entry in data.values():
                        if entry['ticker'].lower() == ticker.lower():
                            self.cik = str(entry['cik_str']).zfill(10) 
                if self.cik is None:
                    print('Failed to request ticker symbol cik.')
                else:
                    print('Sending request to SEC EDGAR API...')
                    time.sleep(1) # be polite to SEC server
                    self.facts = safe_status_get(url=f"https://data.sec.gov/api/xbrl/companyfacts/CIK{self.cik}.json", headers=self.HEADERS)
                    if self.facts is None:
                        print("Failed to fetch filing data from SEC.")
            else:
                bulk_cik_path = Path('bulk_data/company_tickers.json')
                with open(bulk_cik_path, 'r') as f:
                    data = json.load(f)
                    if data:
                        for entry in data.values():
                            if entry['ticker'].lower() == ticker.lower():
                                self.cik = str(entry['cik_str']).zfill(10) 
                if self.cik is None:
                    print('Failed to request ticker symbol cik.')
                else:
                    bulk_data_path = Path(f"bulk_data/companyfacts/CIK{self.cik}.json")
                    if not bulk_data_path.exists():
                        print(f"Error: {bulk_data_path}\nDoes not exist.")
                        return None
                    with open(bulk_data_path, 'r') as f:
                        self.facts = json.load(f)
                    if self.facts is None:
                        print("Failed to fetch filing from bulk SEC data.")
        except Exception as e:
            print(f"Failed to request data. Use request option if you have not downloaded the bulk data.\nError code:\n{e}")

    def get_metrics(self) -> pd.DataFrame | None:
        try:
            if self.facts is not None:
                for key in keylist.key_list_shares:
                    if key in self.facts['facts']['us-gaap'].keys():
                        shares_outstanding = self.facts['facts']['us-gaap'][key]['units']['shares'][-1]
                        form = shares_outstanding['form']
                        filed = shares_outstanding['filed']
                        shares_outstanding = shares_outstanding['val']
                        if shares_outstanding is not None and shares_outstanding > 0:
                            break
                else:
                    shares_outstanding = nan
                    form = None
                    filed = None
                for key in keylist.key_list_cash:
                    if key in self.facts['facts']['us-gaap'].keys():
                        cash = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        cash = cash['val']
                        break
                else:
                    cash = nan
                for key in keylist.key_list_debt:
                    if key in self.facts['facts']['us-gaap'].keys():
                        debt = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        debt = debt['val']
                        break
                else:
                    debt = nan
                for key in keylist.key_list_revenue:
                    if key in self.facts['facts']['us-gaap'].keys():
                        revenue = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        revenue = revenue['val']
                        break
                else:
                    revenue = nan
                for key in keylist.key_list_cogs:
                    if key in self.facts['facts']['us-gaap'].keys():
                        cogs = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        cogs = cogs['val']
                        break
                else:
                    cogs = nan
                for key in keylist.key_list_gross_profit:
                    if key in self.facts['facts']['us-gaap'].keys():
                        gross_profit = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        gross_profit = gross_profit['val']
                        break
                else:
                    try:
                        gross_profit = revenue - cogs
                    except:
                        gross_profit = nan
                for key in keylist.key_list_operating_income:
                    if key in self.facts['facts']['us-gaap'].keys():
                        operating_income = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        operating_income = operating_income['val']
                        break
                else:
                    operating_income = nan
                for key in keylist.key_list_income:
                    if key in self.facts['facts']['us-gaap'].keys():
                        income = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        income = income['val']
                        break
                else:
                    income = nan
                for key in keylist.key_list_assets:
                    if key in self.facts['facts']['us-gaap'].keys():
                        assets = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        assets = assets['val']
                        break
                else:
                    assets = nan
                for key in keylist.key_list_liability:
                    if key in self.facts['facts']['us-gaap'].keys():
                        liability = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        liability = liability['val']
                        break
                else:
                    liability = nan
                for key in keylist.key_list_opex:
                    if key in self.facts['facts']['us-gaap'].keys():
                        opex = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        opex = opex['val']
                        break
                else:
                    opex = nan
                for key in keylist.key_list_capex:
                    if key in self.facts['facts']['us-gaap'].keys():
                        capex = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        capex = capex['val']
                        break
                else:
                    capex = nan
                for key in keylist.key_list_ocf:
                    if key in self.facts['facts']['us-gaap'].keys():
                        ocf = self.facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        ocf = ocf['val']
                        break
                else:
                    ocf = nan
                for key in keylist.key_list_eps:
                    if key in self.facts['facts']['us-gaap'].keys():
                        eps = self.facts['facts']['us-gaap'][key]['units']['USD/shares'][-1]
                        eps = eps['val']
                        break
                else:
                    eps = nan

                df: pd.DataFrame = pd.DataFrame([
                    ['Form', form],
                    ['Filed', filed],
                    ['Shares Outstanding', shares_outstanding],
                    ['Cash', cash],
                    ['Debt', debt],
                    ['Revenue', revenue],
                    ['COGS', cogs],
                    ['Gross Profit', gross_profit],
                    ['EBIT', operating_income],
                    ['Net Income', income],
                    ['Assets', assets],
                    ['Liabilities', liability],
                    ['Equity', assets - liability],
                    ['OpEx', opex],
                    ['CapEx', capex],
                    ['OCF', ocf],
                    ['FCF', ocf - capex],
                    ['EPS', eps],
                ])
                df.set_index(0, inplace=True)
                df.index.name = 'Metrics:'
                df.columns = [self.ticker]
                return df
            else:
                print("Error: filing data failed to initialize.")
                return None
        except Exception as e:
            print(f"Failed to request company facts:\n{e}")
            return None

    def get_dcf_metrics(self):
        try:
            if self.facts is not None:
                keys = self.facts['facts']['us-gaap'].keys()
                shares = None
                df_capex = None
                df_ocf = None
                for key in keylist.key_list_shares:
                    try:
                        if key in keys:
                            data = self.facts['facts']['us-gaap'][key]['units']['shares'][-40:]
                            result = [{'val': entry['val'], 'filed': entry['filed']} for entry in data]
                            df = pd.DataFrame(result)
                            df['filed'] = pd.to_datetime(df['filed'])
                            df = df.sort_values('filed', ascending=True)
                            df = df.drop_duplicates(subset='filed', keep='first')
                            df_shares = df.tail(20)
                            shares = df_shares.iloc[-1]['val']
                            break
                    except:
                        continue
                for key in keylist.key_list_capex:
                    try:
                        if key in keys:
                            data = self.facts['facts']['us-gaap'][key]['units']['USD'][-40:]
                            result = [{'val': entry['val'], 'filed': entry['filed']} for entry in data]
                            df = pd.DataFrame(result)
                            df['filed'] = pd.to_datetime(df['filed'])
                            df = df.sort_values('filed', ascending=True)
                            df = df.drop_duplicates(subset='filed', keep='first')
                            df_capex = df.tail(20)
                            break
                    except:
                        continue
                for key in keylist.key_list_ocf:
                    try:
                        if key in keys:
                            data = self.facts['facts']['us-gaap'][key]['units']['USD'][-40:]
                            result = [{'val': entry['val'], 'filed': entry['filed']} for entry in data]
                            df = pd.DataFrame(result)
                            df['filed'] = pd.to_datetime(df['filed'])
                            df = df.sort_values('filed', ascending=True)
                            df = df.drop_duplicates(subset='filed', keep='first')
                            df_ocf = df.tail(20)
                            break
                    except:
                        continue
                if isinstance(df_ocf, pd.DataFrame) and isinstance(df_capex, pd.DataFrame):
                    df_fcf = pd.DataFrame()
                    df_fcf['date'] = df_ocf['filed']
                    df_fcf['ocf'] = df_ocf['val']
                    df_fcf['capex'] = df_capex['val']
                    df_fcf['fcf'] = df_fcf['ocf'] - df_fcf['capex']
                    df_fcf.set_index('date', inplace=True)
                    return df_fcf, shares
                else:
                    print("data not found")
                    return None, None
            else:
                print("Error: filing data failed to initialize.")
                return None, None
        except Exception as e:
            print(f"Failed to request company facts:\n{e}")
            return None, None

