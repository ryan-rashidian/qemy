# cli_helper is for the 'help' command in cli.py
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
        ("filing", "Fetches latest SEC filing (10K/10Q)"),
        ("price", "Fetches stock price data"),
        ("table", "Shows and saves current filings"),
        ("watchlist", "Shows and saves current tickers"),
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
        ("plot_netex", ""),
        ("plot_nfp", ""),
        ("plot_price", ""),
        ("plot_sent", ""),
        ("plot_unem", ""),
    ])
    print_help_table(" General Commands: ", [
        ("calc", "Simple Calculator"),
        ("clear", ""),
        ("exit", ""),
    ])
    print_help_table(" Additional Info: ", [
        ("flags", "place-holder"),
        ("units", "place-holder"),
        ("info", "place-holder"),
    ])

    print("\nType 'help <command>' for more details.\n")

