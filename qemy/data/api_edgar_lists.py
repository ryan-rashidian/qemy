
key_list_shares = [
    'CommonStockSharesOutstanding',
    'WeightedAverageNumberOfSharesOutstandingBasic',
    'WeightedAverageNumberOfDilutedSharesOutstanding',
    'EntityCommonStockSharesOutstanding',
]

key_list_cash = [
    'CashAndCashEquivalentsAtCarryingValue',
    'Cash',
    'CashCashEquivalentsAndShortTermInvestments',
]

key_list_debt = [
    ### total debt
    'Debt',
    'DebtLongtermAndShorttermCombinedAmount',
    'LongTermDebtAndCapitalLeaseObligations',
    'DebtSecurities',
    'TotalDebt',
]
key_list_debt_long = [
    ### long term debt
    'LongTermDebtAndLeaseObligation',
    'LongTermDebtNoncurrent',
    'LongTermDebtCurrent',
    'LongTermDebt', ### total current and non-current, component of a component. needs own check.
]
key_list_debt_short = [
    ### short term debt
    'ShortTermDebtAndCurrentPortionOfLongTermDebt',
    'ShortTermDebt',
    'DebtCurrent',
    'CurrentPortionOfLongTermDebt',
    'ShortTermBorrowings',
]
key_list_debt_fallbacks = [
    ### legacy terms, fallback logic
    'NotesPayable',
    'NotesPayableRelatedPartiesCurrentAndNoncurrent',
    'ConvertibleDebtNoncurrent',
    'OperatingLeaseLiability',
    'DebtInstrumentCarryingAmount',
    'FinanceLeaseLiability',
    'FinanceLeaseObligation',
]

key_list_revenue = [
    'Revenue',
    'RevenueNet',
    'RevenueFromContractWithCustomerExcludingAssessedTax',
    'SalesRevenueNet',
    'Revenues',
    'TotalRevenues',
    'NetSales',
    'SalesRevenueGoodsNet',
]

key_list_cogs = [
    'CostOfRevenue',
    'CostOfGoodsAndServicesSold',
    'CostOfGoodsSold',
    'CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization',
    'CostOfSales',
    'CostsOfSales',
    'CostOfGoodsSoldExcludingDepreciation',
    'CostsAndExpensesApplicableToRevenue',
    'CostsAndExpensesDirect',
    'ProgrammingCosts',
    'CostsAndExpenses', # suspect
]

key_list_gross_profit = [
    'GrossProfit',
    'GrossProfitLoss',
    'GrossProfitLossAvailableToCommonStockholders',
]

key_list_operating_income = [
    'OperatingIncomeLoss',
    'OperatingIncomeLossBeforeOtherIncomeExpense',
    'OperatingIncomeLossBeforeInterestAndIncomeTaxes',
    'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
    'IncomeLossFromOperations',
    'IncomeLossFromContinuingOperations',
    'OperatingIncomeLossFromContinuingOperations',
]

key_list_income = [
    'NetIncomeLossAvailableToCommonStockholdersBasic',
    'NetIncomeLoss',
    'NetIncomeLossFromContinuingOperationsAvailableToCommonShareholdersBasic',
    'ProfitLoss',
    'NetIncomeLossIncludingPortionAttributableToNoncontrollingInterest',
]

key_list_assets = [
    'Assets',
]

key_list_liability = [
    'Liabilities',
    'LiabilitiesCurrent',
]

key_list_opex = [
    'OperatingExpenses',
    'OperatingCostsAndExpenses',
    'CostsAndExpenses',
    'NoninterestExpense',
    'GeneralAndAdministrativeExpense',
    'EngineeringAndProductDevelopmentExpense',
    'ResearchAndDevelopmentExpense',
    'SellingGeneralAndAdministrativeExpense',
]

key_list_capex = [
    'PaymentsToAcquirePropertyPlantAndEquipment',
    'CapitalExpenditures',
    'PaymentsToAcquireProductiveAssets',
    'PaymentsForProceedsFromProductiveAssets',
    'PaymentsToAcquireOtherPropertyPlantAndEquipment',
    'CapitalExpendituresIncurredButNotYetPaid',
]

key_list_ocf = [
    'NetCashProvidedByUsedInOperatingActivities',
    'NetCashProvidedByUsedInOperatingActivitiesContinuingOperations',
    'NetCashProvidedByUsedInOperatingActivitiesNoncontrollingInterest',
    'CashProvidedByUsedInOperatingActivities',
    'NetCashProvidedByOperatingActivities',
    'NetCashFlowFromOperatingActivities',
]

key_list_eps = [
    'EarningsPerShareDiluted',
    'EarningsPerShareBasic',
    'EarningsPerShareDilutedIncludingExtraordinaryItems',
    'EarningsPerShareBasicIncludingExtraordinaryItems',
]

key_lists = {
    'shares': key_list_shares,
    'cash': key_list_cash,
    'rev': key_list_revenue,
    'cogs': key_list_cogs,
    'gprofit': key_list_gross_profit,
    'ebit': key_list_operating_income,
    'netinc': key_list_income,
    'assets': key_list_assets,
    'liab': key_list_liability,
    'opex': key_list_opex,
    'capex': key_list_capex,
    'ocf': key_list_ocf,
    'eps': key_list_eps,
}

