import os
from math import nan
import requests
import pandas as pd

class SEC_Filings:
    def __init__(self, ticker):
        self.HEADERS = {'User-Agent': os.getenv('EDGAR_USER_AGENT')} 
        self.ticker = ticker.upper().strip()
        try:
            url = 'https://www.sec.gov/files/company_tickers.json'
            data = requests.get(url=url, headers=self.HEADERS)
            code = data.status_code
            data = data.json()
            if code == 200:
                for entry in data.values():
                    if entry['ticker'].lower() == ticker.lower():
                        self.cik = str(entry['cik_str']).zfill(10) 
            else:
                print(f"Failed to retrieve cik data. Status code:\n{code}")
        except Exception as e:
            print(f"Failed to request cik. Error code:\n{e}")

    def get_metrics(self):
        key_form = None
        key_filed = None
        key_list_shares = [
            'CommonStockSharesOutstanding',
            'WeightedAverageNumberOfSharesOutstandingBasic',
        ]
        key_shares = None
        key_list_cash = [
            'CashAndCashEquivalentsAtCarryingValue',
            'Cash',
        ]
        key_cash = None
        key_list_debt = [
            'DebtLongtermAndShorttermCombinedAmount',
            'DebtInstrumentCarryingAmount',
            'LongTermDebt',
            'LongTermDebtNoncurrent',
            'LongTermDebtCurrent',
            'DebtCurrent',
            'NotesPayable',
            'NotesPayableRelatedPartiesCurrentAndNoncurrent',
            'ConvertibleDebtNoncurrent',
            'OperatingLeaseLiability',
        ]
        key_debt = None
        key_list_revenue = [
            'Revenues',
            'SalesRevenueNet',
            'RevenueFromContractWithCustomerExcludingAssessedTax',
            'OperatingIncomeLoss',
        ]
        key_revenue = None
        key_list_cogs = [
            'CostOfRevenue',
            'CostOfGoodsAndServicesSold',
            'CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization',
            'CostsAndExpenses',
            'InterestExpense',
        ]
        key_cogs = None
        key_list_income = [
            'NetIncomeLossAvailableToCommonStockholdersBasic',
            'NetIncomeLoss',
        ]
        key_income = None
        key_list_assets = [
            'Assets',
        ]
        key_assets = None
        key_list_liability = [
            'Liabilities',
            'LiabilitiesCurrent',
        ]
        key_liability = None
        key_list_opex = [
            'OperatingExpenses',
            'CostsAndExpenses',
            'OperatingCostsAndExpenses',
            'NoninterestExpense',
            'ResearchAndDevelopmentExpense',
            'SellingGeneralAndAdministrativeExpense',
        ]
        key_opex = None
        key_list_capex = [
            'PaymentsToAcquirePropertyPlantAndEquipment',
            'CapitalExpenditures',
            'PaymentsToAcquireProductiveAssets',
            'PaymentsForProceedsFromProductiveAssets',
            'PaymentsToAcquireOtherPropertyPlantAndEquipment',
        ]
        key_capex = None
        key_list_eps = [
            'EarningsPerShareDiluted',
            'EarningsPerShareBasic',
        ]
        key_eps = None

        try:
            facts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{self.cik}.json", headers=self.HEADERS)
            code = facts.status_code
            facts = facts.json()
            if code == 200:
                for key in key_list_shares:
                    if key in facts['facts']['us-gaap'].keys():
                        key_shares = key
                        shares_outstanding = facts['facts']['us-gaap'][key_shares]['units']['shares'][-1]
                        key_form = shares_outstanding['form']
                        key_filed = shares_outstanding['filed']
                        shares_outstanding = shares_outstanding['val']
                        if shares_outstanding is not None and shares_outstanding > 0:
                            break
                else:
                    shares_outstanding = nan
                for key in key_list_cash:
                    if key in facts['facts']['us-gaap'].keys():
                        key_cash = key
                        cash = facts['facts']['us-gaap'][key_cash]['units']['USD'][-1]
                        cash = cash['val']
                        break
                else:
                    cash = nan
                for key in key_list_debt:
                    if key in facts['facts']['us-gaap'].keys():
                        key_debt = key
                        debt = facts['facts']['us-gaap'][key_debt]['units']['USD'][-1]
                        debt = debt['val']
                        break
                else:
                    debt = nan
                for key in key_list_revenue:
                    if key in facts['facts']['us-gaap'].keys():
                        key_revenue = key
                        revenue = facts['facts']['us-gaap'][key_revenue]['units']['USD'][-1]
                        revenue = revenue['val']
                        break
                else:
                    revenue = nan
                for key in key_list_cogs:
                    if key in facts['facts']['us-gaap'].keys():
                        key_cogs = key
                        cogs = facts['facts']['us-gaap'][key_cogs]['units']['USD'][-1]
                        cogs = cogs['val']
                        break
                else:
                    cogs = nan
                for key in key_list_income:
                    if key in facts['facts']['us-gaap'].keys():
                        key_income = key
                        income = facts['facts']['us-gaap'][key_income]['units']['USD'][-1]
                        income = income['val']
                        break
                else:
                    income = nan
                for key in key_list_assets:
                    if key in facts['facts']['us-gaap'].keys():
                        key_assets = key
                        assets = facts['facts']['us-gaap'][key_assets]['units']['USD'][-1]
                        assets = assets['val']
                        break
                else:
                    assets = nan
                for key in key_list_liability:
                    if key in facts['facts']['us-gaap'].keys():
                        key_liability = key
                        liability = facts['facts']['us-gaap'][key_liability]['units']['USD'][-1]
                        liability = liability['val']
                        break
                else:
                    liability = nan
                for key in key_list_opex:
                    if key in facts['facts']['us-gaap'].keys():
                        key_opex = key
                        opex = facts['facts']['us-gaap'][key_opex]['units']['USD'][-1]
                        opex = opex['val']
                        break
                else:
                    opex = nan
                for key in key_list_capex:
                    if key in facts['facts']['us-gaap'].keys():
                        key_capex = key
                        capex = facts['facts']['us-gaap'][key_capex]['units']['USD'][-1]
                        capex = capex['val']
                        break
                else:
                    capex = nan
                for key in key_list_eps:
                    if key in facts['facts']['us-gaap'].keys():
                        key_eps = key
                        eps = facts['facts']['us-gaap'][key_eps]['units']['USD/shares'][-1]
                        eps = eps['val']
                        break
                else:
                    eps = nan

                df = pd.DataFrame([
                    ['Form', key_form],
                    ['Filed', key_filed],
                    ['Shares Outstanding', shares_outstanding],
                    ['Cash', cash],
                    ['Debt', debt],
                    ['Revenue', revenue],
                    ['COGS', cogs],
                    ['Net Income', income],
                    ['Assets', assets],
                    ['Liabilities', liability],
                    ['OpEx', opex],
                    ['CapEx', capex],
                    ['EPS', eps],
                ])
                df.set_index(0, inplace=True)
                df.columns = ['Value']
                return df
            else:
                print(f"Failed to retrieve data. Status code:\n{code}")
        except Exception as e:
            print(f"Failed to request company facts:\n{e}")

