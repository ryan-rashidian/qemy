import os
import time
import json
from math import nan
import pandas as pd
from pathlib import Path
from . import api_edgar_lists as keylist
from qemy.utils.utils_fetch import safe_status_get
from qemy.utils.parse_filing import get_metric_df

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
                root_dir = Path(__file__).resolve().parents[2]
                bulk_cik_path = root_dir / 'bulk_data' / 'company_tickers.json'
                with open(bulk_cik_path, 'r') as f:
                    data = json.load(f)
                    if data:
                        for entry in data.values():
                            if entry['ticker'].lower() == ticker.lower():
                                self.cik = str(entry['cik_str']).zfill(10) 
                if self.cik is None:
                    print('Failed to request ticker symbol cik.')
                else:
                    bulk_data_path = root_dir / 'bulk_data' / 'companyfacts' / f"CIK{self.cik}.json"
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

                df_shares = get_metric_df(facts=self.facts, keylist=keylist.key_list_shares, quarters=10)
                if not df_shares.empty:
                    latest = df_shares.iloc[-1]
                    shares_outstanding = latest['val']
                    form = latest['form']
                    filed = latest['filed']
                else:
                    shares_outstanding = nan
                    form = None
                    filed = None
                df_cash = get_metric_df(self.facts, keylist.key_list_cash, quarters=10)
                cash = df_cash.iloc[-1]['val'] if not df_cash.empty else nan
                df_debt = get_metric_df(self.facts, keylist.key_list_debt, quarters=10)
                debt = df_debt.iloc[-1]['val'] if not df_debt.empty else nan
                df_revenue = get_metric_df(self.facts, keylist.key_list_revenue, quarters=10)
                revenue = df_revenue.iloc[-1]['val'] if not df_revenue.empty else nan
                df_cogs = get_metric_df(self.facts, keylist.key_list_cogs, quarters=10)
                cogs = df_cogs.iloc[-1]['val'] if not df_cogs.empty else nan
                df_gross_profit = get_metric_df(self.facts, keylist.key_list_gross_profit, quarters=10)
                gross_profit = df_gross_profit.iloc[-1]['val'] if not df_gross_profit.empty else revenue - cogs
                df_operating_income = get_metric_df(self.facts, keylist.key_list_operating_income, quarters=10)
                operating_income = df_operating_income.iloc[-1]['val'] if not df_operating_income.empty else nan
                df_income = get_metric_df(self.facts, keylist.key_list_income, quarters=10)
                income = df_income.iloc[-1]['val'] if not df_income.empty else nan
                df_assets = get_metric_df(self.facts, keylist.key_list_assets, quarters=10)
                assets = df_assets.iloc[-1]['val'] if not df_assets.empty else nan
                df_liability = get_metric_df(self.facts, keylist.key_list_liability, quarters=10)
                liability = df_liability.iloc[-1]['val'] if not df_liability.empty else nan
                df_opex = get_metric_df(self.facts, keylist.key_list_opex, quarters=10)
                opex = df_opex.iloc[-1]['val'] if not df_opex.empty else nan
                df_capex = get_metric_df(self.facts, keylist.key_list_capex, quarters=10)
                capex = df_capex.iloc[-1]['val'] if not df_capex.empty else nan
                df_ocf = get_metric_df(self.facts, keylist.key_list_ocf, quarters=10)
                ocf = df_ocf.iloc[-1]['val'] if not df_ocf.empty else nan
                df_eps = get_metric_df(self.facts, keylist.key_list_eps, quarters=10)
                eps = df_eps.iloc[-1]['val'] if not df_eps.empty else nan

                df: pd.DataFrame = pd.DataFrame([
                    ['Form', form],
                    ['Filed', filed],
                    ['Shares Outstanding', shares_outstanding],
                    ['Cash & Equivalents', cash],
                    ['Total Debt', debt],
                    ['Net Debt', debt - cash],
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

    def get_metric_history(self, key=keylist.key_list_eps, quarters=20):
        try:
            if self.facts is not None:

                df_metric_hist = get_metric_df(self.facts, keylist=key, quarters=quarters * 4)
                metric = df_metric_hist.tail(quarters)
                metric.set_index('filed', inplace=True)
                if isinstance(metric, pd.DataFrame):
                    return metric
                else:
                    print("get_metric_history\nData Not Found.")
                    return None

        except Exception as e:
            print(f"Failed to request company facts:\n{e}")
            return None

    def get_dcf_metrics(self):
        try:
            if self.facts is not None:

                df_shares = get_metric_df(self.facts, keylist.key_list_shares, quarters=40)
                df_shares = df_shares.drop_duplicates('filed').sort_values('filed').tail(20)
                shares = df_shares.iloc[-1]['val'] if not df_shares.empty else nan
                df_cash = get_metric_df(self.facts, keylist.key_list_cash, quarters=10)
                cash = df_cash.iloc[-1]['val'] if not df_cash.empty else nan
                df_debt = get_metric_df(self.facts, keylist.key_list_debt, quarters=10)
                debt = df_debt.iloc[-1]['val'] if not df_debt.empty else nan
                net_debt = debt - cash

                df_capex = get_metric_df(self.facts, keylist.key_list_capex, quarters=40)
                df_capex  = df_capex.drop_duplicates('filed').sort_values('filed').tail(20)
                df_ocf = get_metric_df(self.facts, keylist.key_list_ocf, quarters=40)
                df_ocf    = df_ocf.drop_duplicates('filed').sort_values('filed').tail(20)

                if isinstance(df_ocf, pd.DataFrame) and isinstance(df_capex, pd.DataFrame):
                    if not df_ocf.empty and not df_capex.empty:
                        df_fcf = pd.merge(df_ocf, df_capex, on='filed', suffixes=('_ocf', '_capex'))
                        df_fcf['fcf'] = df_fcf['val_ocf'] - df_fcf['val_capex']
                        df_fcf.rename(columns={'filed': 'date'}, inplace=True)
                        df_fcf.set_index('date', inplace=True)
                    else:
                        df_fcf = None
                    return df_fcf, shares, net_debt
                else:
                    print("get_dcf_metrics\nData Not Found")
                    return None, None, None

            else:
                print("Error: filing data failed to initialize.")
                return None, None, None
        except Exception as e:
            print(f"Failed to request company facts:\n{e}")
            return None, None, None

