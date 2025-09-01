"""Help information for API EDGAR Qemy CLI commands."""

help_f = """Category: SEC Filings
Fetch a summary of the latest filing for a given ticker.

Usage: f <TICKER>
"""

help_fc = """Category: SEC Filings
Fetch historical data for given ticker and concept.

Concepts (command : 'description/definition')
_____________________________________________

    shares      :    'Shares Outstanding'
    assets      :    'Assets'
    cash        :    'Cash & Equivalents'
    apay        :    'Accounts Payable'
    arec        :    'Accounts Receivable'
    marsec      :    'Marketable Securities'
    ppe         :    'PP&E'
    inven       :    'Inventory'
    goodw       :    'Goodwill'
    debt        :    'Debt'
    sdebt       :    'Shortterm Debt'
    ldebt       :    'Longterm Debt'
    liab        :    'Total Liabilities'
    equity      :    'Stockholders Equity'
    ocf         :    'Operating Cash Flow'
    netcashf    :    'Net Cash: Financing'
    netcashi    :    'Net Cash: Investing'
    capex       :    'CAPEX'
    revenue     :    'Revenue'
    cogs        :    'COGS'
    gprofit     :    'Gross Profit'
    randd       :    'R&D'
    ganda       :    'G&A'
    opinc       :    'Operating Income'
    netinc      :    'Net Income'
    opex        :    'OPEX'
    epsb        :    'EPS Basic'
    epsd        :    'EPS Diluted'

Quarters (Defaults to 8)
________________________

    Number of quarters to fetch.
    Should be a whole number value after defining the concept.

    Example: fc <TICKER> assets 20
        - This example would fetch 20 quarters (5 years) of asset data.

Usage: fc <TICKER> <CONCEPT> <QUARTERS>
"""

help_fsync = """Category: SEC Filings
Download SEC bulk data from within Qemy CLI.
Doing this allows will enable Qemy to access SEC filing data locally.

    The benefits of this include:
        - Faster loading times while requesting data
        - Ability to access filing data without requests (offline)

This command will also overwrite previously downloaded data.

    Content will be automatically un-zipped into Qemy's root directory.
        - Download = ~2GB (zipped)
        - Size on disk = ~20GB (un-zipped)
        - Location = /qemy/bulk_data/

It may take a few minutes depending on your connection.
If the download process is interrupted, run fsync again for a clean install.

According to the SEC website (sec.gov), bulk data is updated daily.
"""

