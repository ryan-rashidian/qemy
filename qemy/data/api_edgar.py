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
                cik_data = safe_status_get(url=url, headers=self.HEADERS)
                if cik_data:
                    for entry in cik_data.values():
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
                    cik_data = json.load(f)
                    if cik_data:
                        for entry in cik_data.values():
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

                df_total_debt = get_metric_df(self.facts, keylist.key_list_debt, quarters=10)
                if df_total_debt.empty:
                    df_debt_long = get_metric_df(self.facts, keylist.key_list_debt_long, quarters=10)
                    df_debt_short = get_metric_df(self.facts, keylist.key_list_debt_short, quarters=10)
                    df_debt_long = df_debt_long.infer_objects()
                    df_debt_short = df_debt_short.infer_objects()
                    df_total_debt = pd.merge(df_debt_long, df_debt_short, 
                                             on='filed', how='outer', 
                                             suffixes=('_long', '_short')).copy()
                    df_total_debt = df_total_debt.infer_objects()
                    df_total_debt = df_total_debt.fillna(0)
                    df_total_debt['val'] = df_total_debt['val_long'] + df_total_debt['val_short']
                    df_total_debt = df_total_debt[['filed', 'val']]
                if df_total_debt.empty:
                    df_total_debt = get_metric_df(self.facts, keylist.key_list_debt_fallbacks, quarters=10)
                if not df_total_debt.empty:
                    df_total_debt = df_total_debt.sort_values('filed').reset_index(drop=True)
                    debt = df_total_debt.iloc[-1]['val']
                else:
                    debt = nan
                if not pd.isna(debt):
                    debt = int(debt)

                if pd.notna(debt) and pd.notna(cash):
                    net_debt = debt - cash
                elif pd.notna(debt):
                    net_debt = debt
                elif pd.notna(cash):
                    net_debt = -cash
                else:
                    net_debt = nan

                df_revenue = get_metric_df(self.facts, keylist.key_list_revenue, quarters=10)
                revenue = df_revenue.iloc[-1]['val'] if not df_revenue.empty else nan

                df_cogs = get_metric_df(self.facts, keylist.key_list_cogs, quarters=10)
                cogs = df_cogs.iloc[-1]['val'] if not df_cogs.empty else nan

                df_gross_profit = get_metric_df(self.facts, keylist.key_list_gross_profit, quarters=10)
                if not df_gross_profit.empty:
                    gross_profit = df_gross_profit.iloc[-1]['val']
                elif not df_gross_profit.empty and not df_cogs.empty:
                    gross_profit = revenue - cogs
                elif not df_revenue.empty:
                    gross_profit = revenue
                else:
                    gross_profit = nan

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

                df_metrics: pd.DataFrame = pd.DataFrame([
                    ['Form', form],
                    ['Filed', filed],
                    ['Shares Outstanding', shares_outstanding],
                    ['Cash & Equivalents', cash],
                    ['Total Debt', debt],
                    ['Net Debt', net_debt],
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
                df_metrics.set_index(0, inplace=True)
                df_metrics.index.name = 'Metrics:'
                df_metrics.columns = [self.ticker]
                return df_metrics

            else:
                print("Error: filing data failed to initialize.")
                return None
        except Exception as e:
            print(f"Failed to request company facts:\n{e}")
            return None

    def get_metric_history(self, key='eps', quarters=20):
        try:
            if self.facts is not None:
                key = key.strip().lower()
                
                if key == 'gprofit':
                    df_gprofit_hist = get_metric_df(self.facts, keylist=keylist.key_list_gross_profit, quarters=quarters * 4)
                    if not df_gprofit_hist.empty:
                        df_gprofit_quarters = df_gprofit_hist.tail(quarters).set_index('filed').copy()
                        return df_gprofit_quarters

                    df_revenue_hist = get_metric_df(self.facts, keylist=keylist.key_list_revenue, quarters=quarters * 4)
                    df_cogs_hist = get_metric_df(self.facts, keylist=keylist.key_list_cogs, quarters=quarters * 4)
                    if df_revenue_hist.empty and df_cogs_hist.empty:
                        print("Fallback failed. Gross Profit metric not found.")
                        return None

                    df_combined = pd.merge(df_revenue_hist, df_cogs_hist, on='filed', how='inner', suffixes=('_rev', '_cogs')).copy()
                    df_combined = df_combined.infer_objects()
                    df_combined = df_combined.dropna(subset=['val_rev'])
                    df_combined['val_cogs'] = df_combined['val_cogs'].fillna(0)
                    df_combined['val'] = df_combined['val_rev'] - df_combined['val_cogs']
                    df_gprofit_quarters = df_combined[['filed', 'val']].tail(quarters).copy()
                    df_gprofit_quarters.set_index('filed', inplace=True)
                    return df_gprofit_quarters

                if key == 'debt':
                    df_total_debt_hist = get_metric_df(self.facts, keylist.key_list_debt, quarters=quarters * 4)
                    if df_total_debt_hist.empty:
                        df_debt_long = get_metric_df(self.facts, keylist.key_list_debt_long, quarters=quarters * 4)
                        df_debt_short = get_metric_df(self.facts, keylist.key_list_debt_short, quarters=quarters * 4)
                        df_total_debt_hist = pd.merge(df_debt_long, df_debt_short, 
                                                      on='filed', how='outer',
                                                      suffixes=('_long', '_short')).copy()
                        df_total_debt_hist = df_total_debt_hist.infer_objects()
                        df_total_debt_hist = df_total_debt_hist.fillna(0)
                        df_total_debt_hist['val'] = df_total_debt_hist['val_long'] + df_total_debt_hist['val_short']
                        df_total_debt_hist = df_total_debt_hist[['filed', 'val']]
                    if df_total_debt_hist.empty:
                        df_total_debt_hist = get_metric_df(self.facts, keylist.key_list_debt_fallbacks, quarters=quarters * 4)
                    df_total_debt_hist = df_total_debt_hist.sort_values('filed').reset_index(drop=True)
                    df_debt_quarters = df_total_debt_hist[['filed', 'val']].tail(quarters).copy()
                    df_debt_quarters.set_index('filed', inplace=True)
                    return df_debt_quarters

                if key == 'netdebt':
                    df_debt_hist = get_metric_df(self.facts, keylist=keylist.key_list_debt, quarters=quarters * 4)
                    df_cash_hist = get_metric_df(self.facts, keylist=keylist.key_list_cash, quarters=quarters * 4)
                    if df_cash_hist.empty and df_debt_hist.empty:
                        print("Net Debt: required metrics not found.")
                        return None

                    df_combined = pd.merge(df_debt_hist, df_cash_hist, on='filed', how='outer', suffixes=('_debt', '_cash')).copy()
                    df_combined = df_combined.infer_objects()
                    df_combined = df_combined.fillna(0)
                    df_combined['val'] = df_combined['val_debt'] - df_combined['val_cash']
                    df_netdebt_quarters = df_combined[['filed', 'val']].tail(quarters).copy()
                    df_netdebt_quarters.set_index('filed', inplace=True)
                    return df_netdebt_quarters

                if key == 'equity':
                    df_assets_hist = get_metric_df(self.facts, keylist=keylist.key_list_assets, quarters=quarters * 4)
                    df_liability_hist = get_metric_df(self.facts, keylist=keylist.key_list_liability, quarters=quarters * 4)
                    if df_assets_hist.empty and df_liability_hist.empty:
                        print("Net Debt: required metrics not found.")
                        return None

                    df_combined = pd.merge(df_assets_hist, df_liability_hist, on='filed', how='outer', suffixes=('_assets', '_liability')).copy()
                    df_combined = df_combined.infer_objects()
                    df_combined = df_combined.fillna(0)
                    df_combined['val'] = df_combined['val_assets'] - df_combined['val_liability']
                    df_equity_quarters = df_combined[['filed', 'val']].tail(quarters).copy()
                    df_equity_quarters.set_index('filed', inplace=True)
                    return df_equity_quarters

                if key == 'fcf':
                    df_ocf_hist = get_metric_df(self.facts, keylist=keylist.key_list_ocf, quarters=quarters * 4)
                    df_capex_hist = get_metric_df(self.facts, keylist=keylist.key_list_capex, quarters=quarters * 4)
                    if df_ocf_hist.empty and df_capex_hist.empty:
                        print("Net Debt: required metrics not found.")
                        return None

                    df_combined = pd.merge(df_ocf_hist, df_capex_hist, on='filed', how='outer', suffixes=('_ocf', '_capex')).copy()
                    df_combined = df_combined.infer_objects()
                    df_combined = df_combined.fillna(0)
                    df_combined['val'] = df_combined['val_ocf'] - df_combined['val_capex']
                    df_fcf_quarters = df_combined[['filed', 'val']].tail(quarters).copy()
                    df_fcf_quarters.set_index('filed', inplace=True)
                    return df_fcf_quarters

                if key in keylist.key_lists:
                    key = keylist.key_lists.get(key)
                    if key is None:
                        print(f"Unknown metric type: {key}")
                        return None

                    df_metric_hist = get_metric_df(self.facts, keylist=key, quarters=quarters * 4)
                    df_metric_quarters = df_metric_hist.tail(quarters).copy()
                    df_metric_quarters.set_index('filed', inplace=True)
                    if isinstance(df_metric_quarters, pd.DataFrame):
                        return df_metric_quarters
                else:
                    print(f"get_metric_history: invalid metric name: {key}")
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
                df_total_debt = get_metric_df(self.facts, keylist.key_list_debt, quarters=10)
                if df_total_debt.empty:
                    df_debt_long = get_metric_df(self.facts, keylist.key_list_debt_long, quarters=10)
                    df_debt_short = get_metric_df(self.facts, keylist.key_list_debt_short, quarters=10)
                    df_total_debt = pd.merge(df_debt_long, df_debt_short, 
                                             on='filed', how='outer', 
                                             suffixes=('_long', '_short')).copy()
                    df_total_debt = df_total_debt.infer_objects()
                    df_total_debt = df_total_debt.fillna(0)
                    df_total_debt['val'] = df_total_debt['val_long'] + df_total_debt['val_short']
                    df_total_debt = df_total_debt[['filed', 'val']]
                if df_total_debt.empty:
                    df_total_debt = get_metric_df(self.facts, keylist.key_list_debt_fallbacks, quarters=10)
                if not df_total_debt.empty:
                    df_total_debt = df_total_debt.sort_values('filed').reset_index(drop=True)
                    debt = df_total_debt.iloc[-1]['val']
                else:
                    debt = nan
                net_debt = debt - cash

                df_capex = get_metric_df(self.facts, keylist.key_list_capex, quarters=40)
                df_capex  = df_capex.drop_duplicates('filed').sort_values('filed').tail(20)

                df_ocf = get_metric_df(self.facts, keylist.key_list_ocf, quarters=40)
                df_ocf    = df_ocf.drop_duplicates('filed').sort_values('filed').tail(20)

                if isinstance(df_ocf, pd.DataFrame) and isinstance(df_capex, pd.DataFrame):
                    if not df_ocf.empty and not df_capex.empty:
                        df_fcf = pd.merge(df_ocf, df_capex, 
                                          on='filed', how='outer', 
                                          suffixes=('_ocf', '_capex')).copy()
                        df_fcf = df_fcf.infer_objects()
                        df_fcf = df_fcf.fillna(0)
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

