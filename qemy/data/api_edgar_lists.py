key_list_shares = [
    'CommonStockSharesOutstanding',
    'WeightedAverageNumberOfSharesOutstandingBasic',
]
key_list_cash = [
    'CashAndCashEquivalentsAtCarryingValue',
    'Cash',
]
key_list_debt = [
    ### total debt
    'DebtLongtermAndShorttermCombinedAmount',
    'Debt'
    'LongTermDebtAndCapitalLeaseObligations'
    ### temporary fallback logic
    'LongTermDebt',
    'LongTermDebtNoncurrent',
    'LongTermDebtCurrent',
    'DebtCurrent',
    'NotesPayable',
    'NotesPayableRelatedPartiesCurrentAndNoncurrent',
    'ConvertibleDebtNoncurrent',
    'OperatingLeaseLiability',
    'DebtInstrumentCarryingAmount',
]
key_list_debt_components = [
    ### long term debt
    'LongTermDebt', ### total current and non-current, component of a component. needs own check.
    'LongTermDebtNoncurrent',
    'LongTermDebtCurrent',
    ### short term debt
    'CurrentPortionOfLongTermDebt',
    'DebtCurrent',
    'ShortTermBorrowings',
    'ShortTermDebt',
    ### legacy terms, fallback logic
    'NotesPayable',
    'NotesPayableRelatedPartiesCurrentAndNoncurrent',
    'ConvertibleDebtNoncurrent',
    'OperatingLeaseLiability',
    'DebtInstrumentCarryingAmount',
]
key_list_revenue = [
    'RevenueFromContractWithCustomerExcludingAssessedTax',
    'SalesRevenueNet',
    'Revenues',
    'TotalRevenues',
    'NetSales',
    'SalesRevenueGoodsNet',
    'OperatingIncomeLoss',
]
key_list_cogs = [
    'CostOfRevenue',
    'CostOfGoodsAndServicesSold',
    'CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization',
    'CostsAndExpenses',
    'InterestExpense',
]
key_list_gross_profit = [
    'GrossProfit',
    'GrossProfitLoss',
    'GrossProfitLossAvailableToCommonStockholders',
]
key_list_operating_income = [
    'OperatingIncomeLoss',
    'OperatingIncomeLossFromContinuingOperations',
    'OperatingIncomeLossBeforeOtherIncomeExpense',
    'OperatingIncomeLossBeforeInterestAndIncomeTaxes',
    'IncomeLossFromOperations',
    'IncomeLossFromContinuingOperations',
]
key_list_income = [
    'NetIncomeLossAvailableToCommonStockholdersBasic',
    'NetIncomeLoss',
    'NetIncomeLossFromContinuingOperationsAvailableToCommonShareholdersBasic',
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
    'CostsAndExpenses',
    'OperatingCostsAndExpenses',
    'NoninterestExpense',
    'ResearchAndDevelopmentExpense',
    'SellingGeneralAndAdministrativeExpense',
]
key_list_capex = [
    'PaymentsToAcquirePropertyPlantAndEquipment',
    'CapitalExpenditures',
    'PaymentsToAcquireProductiveAssets',
    'PaymentsForProceedsFromProductiveAssets',
    'PaymentsToAcquireOtherPropertyPlantAndEquipment',
]
key_list_ocf = [
    'NetCashProvidedByUsedInOperatingActivities',
    'NetCashProvidedByUsedInOperatingActivitiesContinuingOperations',
    'NetCashProvidedByUsedInOperatingActivitiesNoncontrollingInterest',
]
key_list_eps = [
    'EarningsPerShareDiluted',
    'EarningsPerShareBasic',
]
