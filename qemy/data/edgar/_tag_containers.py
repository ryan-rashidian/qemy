"""Containers of XBRL taxonomy tags for EDGAR API company concepts.

This module is used to search for concepts keys.
Tuple order reflects relevance/priority from most -> least.
Tag strings with low priority may include fall-back, or component metrics. 
"""

# === Concepts ===

### Shares Outstanding
tag_shares_outstanding = (
    'CommonStockSharesOutstanding',
    'WeightedAverageNumberOfSharesOutstandingBasic',
    'WeightedAverageNumberOfShareOutstandingBasicAndDiluted',
    'WeightedAverageNumberOfDilutedSharesOutstanding',
    'EntityCommonStockSharesOutstanding',
)

## === Balance Sheet ===

### Total Assets
tag_total_assets = (
    'Assets',
)

### Cash and Cash Equivalents
tag_cash_equiv = (
    'CashAndCashEquivalentsAtCarryingValue',
    'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents',
    'Cash',
    'CashCashEquivalentsAndShortTermInvestments',
)

### Property Plant and Equipment (PP&E)
tag_ppande = (
    'PropertyPlantAndEquipmentNet',
    'PropertyPlantAndEquipmentGross',
)

### Inventory
tag_inventory = (
    'InventoryNet',
)

### Goodwill
tag_goodwill = (
    'Goodwill',
)

### Total Debt
tag_debt = (
    'Debt',
    'DebtLongtermAndShorttermCombinedAmount',
    'LongTermDebtAndCapitalLeaseObligations',
    'DebtSecurities',
    'TotalDebt',
    # Legacy tags
    'NotesPayable',
    'NotesPayableRelatedPartiesCurrentAndNoncurrent',
    'ConvertibleDebtNoncurrent',
    'OperatingLeaseLiability',
    'DebtInstrumentCarryingAmount',
    'FinanceLeaseLiability',
    'FinanceLeaseObligation',
)

### Short Term Debt
tag_short_term_debt = (
    'ShortTermDebtAndCurrentPortionOfLongTermDebt',
    'ShortTermDebt',
    'DebtCurrent',
    'CurrentPortionOfLongTermDebt',
    'ShortTermBorrowings',
)

### Long Term Debt
tag_long_term_debt = (
    'LongTermDebt',
    'LongTermDebtAndLeaseObligation',
    'LongTermDebtNoncurrent',
    'LongTermDebtCurrent',
)

### Total Liabilities
tag_total_liabilities = (
    'Liabilities',
    'LiabilitiesCurrent',
)

### Stockholders' Equity
tag_stockholders_equity = (
    'StockholdersEquity',
    'CommonStockEquity',
    'TotalEquity',
    'TotalStockholdersEquity',
    'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest',
    'PartnersCapital',
    'MemberEquity',
)

balance_sheet = {
    'Assets': tag_total_assets,
    'Cash & Equivalents': tag_cash_equiv,
    'PP&E': tag_ppande,
    'Inventory': tag_inventory,
    'Goodwill': tag_goodwill,
    'Debt': tag_debt,
    'Shortterm Debt': tag_short_term_debt,
    'Longterm Debt': tag_long_term_debt,
    'Total Liabilities': tag_total_liabilities,
    'Stockholders Equity': tag_stockholders_equity
}

## === Cash Flow Statement ===

### Net Cash from Operating Activities (OCF)
tag_cash_operating = (
    'NetCashProvidedByUsedInOperatingActivities',
    'NetCashProvidedByUsedInOperatingActivitiesContinuingOperations',
    'NetCashProvidedByUsedInOperatingActivitiesNoncontrollingInterest',
    'CashProvidedByUsedInOperatingActivities',
    'NetCashProvidedByOperatingActivities',
    'NetCashFlowFromOperatingActivities',
)

### Net Cash from Financing Activities
tag_cash_financing = (
    'NetCashProvidedByUsedInFinancingActivities',
)

### Net Cash from Investing Activities
tag_cash_investing = (
    'NetCashProvidedByUsedInInvestingActivities',
)

### Capital Expenditure (CAPEX)
tag_capex = (
    'PaymentsToAcquirePropertyPlantAndEquipment',
    'CapitalExpenditures',
    'PaymentsToAcquireProductiveAssets',
    'PaymentsForProceedsFromProductiveAssets',
    'PaymentsToAcquireOtherPropertyPlantAndEquipment',
    'CapitalExpendituresIncurredButNotYetPaid',
)

cash_flow_statement = {
    'Operating Cash Flow': tag_cash_operating,
    'Net Cash: Financing': tag_cash_financing,
    'Net Cash: Investing': tag_cash_investing,
    'CAPEX': tag_capex
}

## === Income Statement ===

### Revenue
tag_revenue = (
    'Revenues',
    'Revenue',
    'RevenueNet',
    'RevenueFromContractWithCustomerExcludingAssessedTax',
    'SalesRevenueNet',
    'TotalRevenues',
    'NetSales',
    'SalesRevenueGoodsNet',
)

### Cost of Goods and Services (COGS)
tag_cogs = (
    'CostOfRevenue',
    'CostOfRevenues',
    'CostOfGoodsAndServicesSold',
    'CostOfGoodsSold',
    'CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization',
    'CostOfSales',
    'CostsOfSales',
    'CostOfGoodsSoldExcludingDepreciation',
    'CostsAndExpensesApplicableToRevenue',
    'CostsAndExpensesDirect',
    'ProgrammingCosts',
)

### Gross Profit
tag_gross_profit = (
    'GrossProfit',
    'GrossProfitLoss',
    'GrossProfitLossAvailableToCommonStockholders',
)

### Research and Development (R&D)
tag_randd = (
    'ResearchAndDevelopmentExpense',
    'EngineeringAndProductDevelopmentExpense',
)

### General and Administrative (G&A)
tag_ganda = (
    'GeneralAndAdministrativeExpense',
    'SellingGeneralAndAdministrativeExpense',
)

### Operating Income / Loss
tag_operating_income = (
    'OperatingIncomeLoss',
    'OperatingIncomeLossBeforeOtherIncomeExpense',
    'OperatingIncomeLossBeforeInterestAndIncomeTaxes',
    'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
    'IncomeLossFromOperations',
    'IncomeLossFromContinuingOperations',
    'OperatingIncomeLossFromContinuingOperations',
)

### Net Income / Loss
tag_net_income = (
    'NetIncomeLoss',
    'NetIncomeLossAvailableToCommonStockholdersBasic',
    'NetIncomeLossFromContinuingOperationsAvailableToCommonShareholdersBasic',
    'ProfitLoss',
    'NetIncomeLossIncludingPortionAttributableToNoncontrollingInterest',
)

### Operating Expenditure (OPEX)
tag_opex = (
    'OperatingExpenses',
    'OperatingCostsAndExpenses',
    'CostsAndExpenses',
    'NoninterestExpense',
    'GeneralAndAdministrativeExpense',
    'EngineeringAndProductDevelopmentExpense',
    'ResearchAndDevelopmentExpense',
    'SellingGeneralAndAdministrativeExpense',
)

### Earnings per Share Basic
tag_eps_basic = (
    'EarningsPerShareBasic',
    'EarningsPerShareBasicIncludingExtraordinaryItems',
)

### Earnings per Share Diluted
tag_eps_diluted = (
    'EarningsPerShareDiluted',
    'EarningsPerShareDilutedIncludingExtraordinaryItems',
)

income_statement = {
    'Revenue': tag_revenue,
    'COGS': tag_cogs,
    'Gross Profit': tag_gross_profit,
    'R&D': tag_randd,
    'G&A': tag_ganda,
    'Operating Income': tag_operating_income,
    'Net Income': tag_net_income,
    'OPEX': tag_opex,
    'EPS Basic': tag_eps_basic,
    'EPS Diluted': tag_eps_diluted
}

# === Meta Containers ===

## Nested dictionary of all tags
filing_tags = {
    'Company': {'Shares Outstanding': tag_shares_outstanding},
    'Balance Sheet': balance_sheet,
    'Cash Flow Statement': cash_flow_statement,
    'Income Statement': income_statement
}

## CLI Command mapping
map_arg = {
    'shares':   ('Company', 'Shares Outstanding'),
    'assets':   ('Balance Sheet', 'Assets'),
    'cash':     ('Balance Sheet', 'Cash & Equivalents'),
    'ppe':      ('Balance Sheet', 'PP&E'),
    'inven':    ('Balance Sheet', 'Inventory'),
    'goodw':    ('Balance Sheet', 'Goodwill'),
    'debt':     ('Balance Sheet', 'Debt'),
    'sdebt':    ('Balance Sheet', 'Shortterm Debt'),
    'ldebt':    ('Balance Sheet', 'Longterm Debt'),
    'liab':     ('Balance Sheet', 'Total Liabilities'),
    'equity':   ('Balance Sheet', 'Stockholders Equity'),
    'ocf':      ('Cash Flow Statement', 'Operating Cash Flow'),
    'netcashf': ('Cash Flow Statement', 'Net Cash: Financing'),
    'netcashi': ('Cash Flow Statement', 'Net Cash: Investing'),
    'capex':    ('Cash Flow Statement', 'CAPEX'),
    'revenue':  ('Income Statement', 'Revenue'),
    'cogs':     ('Income Statement', 'COGS'),
    'gprofit':  ('Income Statement', 'Gross Profit'),
    'randd':    ('Income Statement', 'R&D'),
    'ganda':    ('Income Statement', 'G&A'),
    'opinc':    ('Income Statement', 'Operating Income'),
    'netinc':   ('Income Statement', 'Net Income'),
    'opex':     ('Income Statement', 'OPEX'),
    'epsb':     ('Income Statement', 'EPS Basic'),
    'epsd':     ('Income Statement', 'EPS Diluted'),
}

