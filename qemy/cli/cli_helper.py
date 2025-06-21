
#================================== HELPER ===================================#

def print_help_table(title, commands):
    print(f"\n{title}")
    print("-" * len(title))
    for cmd, desc in commands:
        print(f"  {cmd.ljust(15)} {desc}")

def help():
    print("\n qemy - Command Reference Table")
    print_help_table(" Command Categories: ", [
        ("econ",    "Enter: 'econ'    to list related commands"),
        ("market",  "Enter: 'market'  to list related commands"),
        ("plugins", "Enter: 'plugins' to list related commands"),
        ("plots",   "Enter: 'plots'   to list related commands"),
    ])
    print_help_table(" Auxiliary Commands: ", [
        ("clear", "or 'cls' to clear screen."),
        ("exit", "or 'q' to exit qemy."),
        ("calc", "Simple calculator with Python syntax"),
        ("bulk_refresh", "Downloads bulk filing data from SEC"),
        ("env_reset", "Deletes current .env file"),
    ])
    print_help_table(" Additional Info: ", [
        ("flags", "- -- Flag command list and descriptions."),
        ("units", "Unit commands for the -u --units flag."),
        ("metrics", "Metric commands for the -m --metric flag."),
        ("info", "Adding soon."),
        ("manual", "In progress/planned."),
    ])
    print("\nEnter '<COMMAND> -h' for more details.\n")

def econ():
    print("\n qemy - Economic Command Reference Table")
    print_help_table(" Econ: ", [
        ("cpi", "Fetches data for - Consumer Price Index"),
        ("gdp", "Fetches data for - Gross Domestic Product"),
        ("indp", "Fetches data for - Industrial Production: Total Index"),
        ("interest", "Fetches data for - Federal Funds Effective Rate"),
        ("jobc", "Fetches data for - Jobless Claims"),
        ("netex", "Fetches data for - Net Export"),
        ("nfp", "Fetches data for - Nonfarm Payrolls"),
        ("rfr", "Fetches data for - Risk Free Rate: 1 Year T-Bill yield"),
        ("sent", "Fetches data for - Consumer Sentiment"),
        ("unem", "Fetches data for - Unemployment Rate"),
    ])
    print("\n")

def market():
    print("\n qemy - Market Command Reference Table")
    print_help_table(" Market:", [
        ("f", "Fetches latest SEC filing (10K/10Q/20F)"),
        ("fmetric", "Fetches filing history for given metric"),
        ("price", "Fetches stock price data"),
        ("quote", "Fetches latest price quote"),
        ("table", "Shows and saves current filings"),
        ("wl", "Show, edit and save current tickers"),
    ])
    print("\n")

def plugins():
    print("\n qemy - Plugin Command Reference Table")
    print_help_table(" Model:", [
        ("m", "Initiates plugin command"),
        ("dcf", "Performs DCF modeling"),
        ("linear_r", "Linear Regression"),
        ("mcarlo", "Monte Carlo simulation"),
        ("Usage:", "m <MODEL>"),
        ("Plugin Help:", "m <MODEL> -h"),
    ])
    print("\n")

def plot():
    print("\n qemy - Plotting Command Reference Table")
    print_help_table(" Plot:", [
        ("plot", "Initiates plot command"),
        ("Commands:", ""),
        ("gdp", ""),
        ("indp", ""),
        ("interest", ""),
        ("jobc", ""),
        ("lr", ""),
        ("mcarlo", ""),
        ("netex", ""),
        ("nfp", ""),
        ("price", ""),
        ("sent", ""),
        ("unem", ""),
    ])
    print("\n")

def flags():
    print("\n qemy - Flags")
    print(" Basic Syntax: <FLAG> <ARGUMENT>")
    print_help_table(" -h --help", [
        ("Info:", "Display the help info for a command."),
        ("Usage:", "<COMMAND> -h"),
        ("Example:", "price -h"),
    ])
    print_help_table(" -p --period", [
        ("D", "Day"),
        ("W", "Week"),
        ("M", "Month"),
        ("Y", "Year"),
        ("Info:", "Specifies a start and end date based on the given period. Start = <Current-Date>, End = <Start - Period>"),
        ("Usage:", "-p <PERIOD>"),
        ("Example:", "-p 3M"),
    ])
    print_help_table(" -plt --plot", [
        ("Info:", "True/False flag to enable plotting feature. Takes no arguments."),
        ("Usage:", "-plt"),
        ("Example:", "m mcarlo -t aapl -p 2y -plt"),
    ])
    print_help_table(" -q --quarter", [
        ("Info:", "Specify number of quarters for SEC filings. 4 = 1 Year."),
        ("Usage:", "-q <QUARTERS>"),
        ("Example:", "fmetric <TICKER> -m <METRIC> -q <QUARTERS>"),
    ])
    print_help_table(" -r --request", [
        ("Info:", "Used to manually send a request to SEC servers."),
        ("Usage:", "-r"),
        ("Example:", "f aapl -r"),
    ])
    print_help_table(" -t --ticker", [
        ("Info:", "Takes ticker symbol as argument."),
        ("Usage:", "-t <TICKER>"),
        ("Example:", "-t aapl"),
    ])
    print_help_table(" -s --save", [
        ("Info:", "True/False flag to enable save feature. Takes no arguments."),
        ("Usage:", "-s"),
        ("Example:", "m mcarlo -t aapl -p 2y -plt -s"),
    ])
    print_help_table(" -u --units", [
        ("Unit arguments:", "lin, chg, ch1, pch, log, etc..."),
        ("Info:", "Transforms data values to given unit type. Enter 'units' for a list and explanation of each argument."),
        ("Usage:", "-u <UNIT>"),
        ("Example:", "-u log"),
    ])
    print_help_table(" -m --metric", [
        ("Info:", "Specify the metric type"),
        ("Usage:", "-m <METRIC>"),
        ("Example:", "fmetric aapl -m eps"),
    ])
    print_help_table(" -n --nums", [
        ("Integer", "Requires integer as argument."),
        ("Info:", "Takes integer argument to specify # of tests to run."),
        ("Usage:", "-n <NUM>"),
        ("Example:", "-n 1000"),
    ])
    print("\n")

def units():
    print("\n qemy - Units")
    print_help_table("Arguments", [
        ("lin", "Default/No transformation"),
        ("chg", "Change"),
        ("ch1", "Change from Year Ago"),
        ("pch", "Percent Change"),
        ("pc1", "Percent Change from Year Ago"),
        ("pca", "Compounded Annual Rate of Change"),
        ("cch", "Continuously Compounded Rate of Change"),
        ("cca", "Continuously Compounded Annual Rate of Change"),
        ("log", "Natural Log"),
    ])
    print("\n")

def metrics():
    print("\n qemy - Metrics")
    print_help_table("Arguments", [
        ("assets", "Total Assets"),
        ("capex", "Capital Expenditure"),
        ("cash", "Total Cash"),
        ("cogs", "Cost of Goods and Service"),
        ("debt", "Total Debt"),
        ("ebit", "Earnings Before Interest and Taxes"),
        ("eps", "Diluted Earnings Per-Share"),
        ("equity", "Total Equity"),
        ("fcf", "Free Cash Flow"),
        ("gprofit", "Gross Profit"),
        ("liab", "Total Liability"),
        ("netdebt", "Net Debt"),
        ("netinc", "Net Income"),
        ("ocf", "Operating Cash Flow"),
        ("opex", "Operating Expenditure"),
        ("rev", "Revenue"),
        ("shares", "Shares Outstanding"),
    ])
    print("\n")

def info(): ### place holder
    print("\n qemy - Information")
    print_help_table(" Usage", [
        ("", ""),
        ("", ""),
    ])
    print("\n")

