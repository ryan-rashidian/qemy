
#================================== HELPER ===================================#

def print_help_table(title, commands):
    print(f"\n{title}")
    print("-" * len(title))
    for cmd, desc in commands:
        print(f"  {cmd.ljust(15)} {desc}")

def help():
    print("\n qemy - Command Reference Table")
    print_help_table(" Market Analysis: ", [
        ("bulk_refresh", "Downloads bulk filing data from SEC"),
        ("dcf", "Performs DCF modeling"),
        ("filing", "Fetches latest SEC filing (10K/10Q/20F)"),
        ("fmetric", "Fetches filing history for given metric"),
        ("lr", "Linear Regression"),
        ("mcarlo", "Monte Carlo simulation"),
        ("price", "Fetches stock price data"),
        ("quote", "Fetches latest price quote"),
        ("table", "Shows and saves current filings"),
        ("wl", "Show, edit and save current tickers"),
    ])
    print_help_table(" Economic Analysis (FRED): ", [
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
    print_help_table(" Plotting / Charts: ", [
        ("plot_cpi", ""),
        ("plot_gdp", ""),
        ("plot_indp", ""),
        ("plot_interest", ""),
        ("plot_jobc", ""),
        ("plot_lr", ""),
        ("plot_mcarlo", ""),
        ("plot_netex", ""),
        ("plot_nfp", ""),
        ("plot_price", ""),
        ("plot_sent", ""),
        ("plot_unem", ""),
    ])
    print_help_table(" Auxiliary Commands: ", [
        ("calc", "Simple Calculator"),
        ("clear", "or 'cls' to clear screen."),
        ("exit", "or 'q' to exit qemy."),
        ("env_reset", "Deletes current .env file"),
    ])
    print_help_table(" Additional Info: ", [
        ("flags", "- -- Flag command list and descriptions."),
        ("units", "Unit commands for the -u --units flag."),
        ("info", "Adding soon."),
        ("manual", "In progress/planned."),
    ])
    print("\nEnter 'help <COMMAND>' for more details.\n")

def flags():
    print("\n qemy - Flags")
    print(" Basic Syntax: <FLAG> <ARGUMENT>")
    print_help_table(" -p --period", [
        ("D", "Day"),
        ("W", "Week"),
        ("M", "Month"),
        ("Y", "Year"),
        ("Info:", "Specifies a start and end date based on the given period. Start = <Current-Date>, End = <Start - Period>"),
        ("Example:", "-p 3M"),
    ])
    print_help_table(" -s --save", [
        ("(yes/no)", "Requires yes or no argument."),
        ("Info:", "Saves a .png or .csv of requested data into /exports/ directory."),
        ("Example:", "-s yes")
    ])
    print_help_table(" -u --units", [
        ("Unit arguments:", "lin, chg, ch1, pch, log, etc..."),
        ("Info:", "Transforms data values to given unit type. Enter 'units' for a list and explanation of each argument."),
        ("Example:", "-u log"),
    ])
    print_help_table(" -n -nums", [
        ("Integer", "Requires integer as argument."),
        ("Info:", "Takes integer argument to specify # of tests to run."),
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

def info(): ### place holder
    print("\n qemy - Information")
    print_help_table(" Usage", [
        ("", ""),
        ("", ""),
    ])
    print("\n")

