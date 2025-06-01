import os
from math import nan
import pandas as pd
from . import api_edgar_lists as keylist
from .utils_fetch import safe_status_get

class SEC_Filings:
    def __init__(self, ticker):
        self.HEADERS = {'User-Agent': os.getenv('EDGAR_USER_AGENT')} 
        self.ticker = ticker.upper().strip()
        self.cik = None
        try:
            url = 'https://www.sec.gov/files/company_tickers.json'
            data = safe_status_get(url=url, headers=self.HEADERS)
            if data:
                for entry in data.values():
                    if entry['ticker'].lower() == ticker.lower():
                        self.cik = str(entry['cik_str']).zfill(10) 
        except Exception as e:
            print(f"Failed to request cik. Error code:\n{e}")

    def get_metrics(self) -> pd.DataFrame | None:
        try:
            facts = safe_status_get(url=f"https://data.sec.gov/api/xbrl/companyfacts/CIK{self.cik}.json", headers=self.HEADERS)
            if facts:
                for key in keylist.key_list_shares:
                    if key in facts['facts']['us-gaap'].keys():
                        shares_outstanding = facts['facts']['us-gaap'][key]['units']['shares'][-1]
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
                    if key in facts['facts']['us-gaap'].keys():
                        cash = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        cash = cash['val']
                        break
                else:
                    cash = nan
                for key in keylist.key_list_debt:
                    if key in facts['facts']['us-gaap'].keys():
                        debt = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        debt = debt['val']
                        break
                else:
                    debt = nan
                for key in keylist.key_list_revenue:
                    if key in facts['facts']['us-gaap'].keys():
                        revenue = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        revenue = revenue['val']
                        break
                else:
                    revenue = nan
                for key in keylist.key_list_cogs:
                    if key in facts['facts']['us-gaap'].keys():
                        cogs = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        cogs = cogs['val']
                        break
                else:
                    cogs = nan
                for key in keylist.key_list_gross_profit:
                    if key in facts['facts']['us-gaap'].keys():
                        gross_profit = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        gross_profit = gross_profit['val']
                        break
                else:
                    try:
                        gross_profit = revenue - cogs
                    except:
                        gross_profit = nan
                for key in keylist.key_list_operating_income:
                    if key in facts['facts']['us-gaap'].keys():
                        operating_income = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        operating_income = operating_income['val']
                        break
                else:
                    operating_income = nan
                for key in keylist.key_list_income:
                    if key in facts['facts']['us-gaap'].keys():
                        income = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        income = income['val']
                        break
                else:
                    income = nan
                for key in keylist.key_list_assets:
                    if key in facts['facts']['us-gaap'].keys():
                        assets = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        assets = assets['val']
                        break
                else:
                    assets = nan
                for key in keylist.key_list_liability:
                    if key in facts['facts']['us-gaap'].keys():
                        liability = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        liability = liability['val']
                        break
                else:
                    liability = nan
                for key in keylist.key_list_opex:
                    if key in facts['facts']['us-gaap'].keys():
                        opex = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        opex = opex['val']
                        break
                else:
                    opex = nan
                for key in keylist.key_list_capex:
                    if key in facts['facts']['us-gaap'].keys():
                        capex = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        capex = capex['val']
                        break
                else:
                    capex = nan
                for key in keylist.key_list_ocf:
                    if key in facts['facts']['us-gaap'].keys():
                        ocf = facts['facts']['us-gaap'][key]['units']['USD'][-1]
                        ocf = ocf['val']
                        break
                else:
                    ocf = nan
                for key in keylist.key_list_eps:
                    if key in facts['facts']['us-gaap'].keys():
                        eps = facts['facts']['us-gaap'][key]['units']['USD/shares'][-1]
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
        except Exception as e:
            print(f"Failed to request company facts:\n{e}")
            return None

