from qemy.core.plot import plot
from qemy.utils.parse_arg import parse_args

#================================== PLOT =====================================#

def plot_price(arg):
    period, ticker = parse_args(arg_str=arg, expected_args=['period', 'ticker'], prog_name='plot_price')

    if isinstance(period, str) and isinstance(ticker, str):
        print(f"Fetching plot chart for: {ticker} daily closing prices, log scaled...")
        try:
            plot.plot_price(ticker=ticker, period=period)
        except Exception as e:
            print(f"Could not fetch plot chart, please try another ticker. Error:\n{e}")
    else:
        print('For valid syntax, Try: plot_price AAPL -p 3M')

def plot_cpi(arg):
    period, save_state, units = parse_args(arg_str=arg, expected_args=['period', 'save', 'units'], prog_name='plot_cpi')
    if not save_state:
        save_state = False
    units = 'pc1' if units is None else units
    
    if isinstance(period, str):
        print(f"Fetching plot chart for CPI inflation: % Change from Year Ago...")
        try:
            plot.plot_cpi(period=period, save=save_state, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_cpi -p 3m -s yes')

def plot_gdp(arg):
    period, save_state, units = parse_args(arg_str=arg, expected_args=['period', 'save', 'units'], prog_name='plot_gdp')
    if not save_state:
        save_state = False
    units = 'pc1' if units is None else units

    if isinstance(period, str):
        print(f"Fetching plot chart for GDP: % Change from Year Ago...")
        try:
            plot.plot_gdp(period=period, save=save_state, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_gdp -p 3M -s yes')

def plot_sent(arg):
    period, save_state, units = parse_args(arg_str=arg, expected_args=['period', 'save', 'units'], prog_name='plot_sent')
    if not save_state:
        save_state = False
    units = 'pch' if units is None else units

    if isinstance(period, str):
        print(f"Fetching plot chart for Sentiment: % Change...")
        try:
            plot.plot_sentiment(period=period, save=save_state, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_sent -p 3M -s yes')

def plot_nfp(arg):
    period, save_state, units = parse_args(arg_str=arg, expected_args=['period', 'save', 'units'], prog_name='plot_nfp')
    if not save_state:
        save_state = False
    units = 'pc1' if units is None else units

    if isinstance(period, str):
        print(f"Fetching plot chart for Non-Farm Payrolls: % Change from Year Ago...")
        try:
            plot.plot_nfp(period=period, save=save_state, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_nfp -p 3M -s yes')

def plot_interest(arg):
    period, save_state, units = parse_args(arg_str=arg, expected_args=['period', 'save', 'units'], prog_name='plot_interest')
    if not save_state:
        save_state = False
    units = 'pc1' if units is None else units

    if isinstance(period, str):
        print(f"Fetching plot chart for Interest rates: % Change from Year Ago...")
        try:
            plot.plot_interest(period=period, save=save_state, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_interest -p 3M -s yes')

def plot_jobc(arg):
    period, save_state, units = parse_args(arg_str=arg, expected_args=['period', 'save', 'units'], prog_name='plot_jobc')
    if not save_state:
        save_state = False
    units = 'pc1' if units is None else units

    if isinstance(period, str):
        print(f"Fetching plot chart for Jobless Claims: % Change from Year Ago...")
        try:
            plot.plot_jobc(period=period, save=save_state, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_jobc -p 3M -s yes')

def plot_unem(arg):
    period, save_state, units = parse_args(arg_str=arg, expected_args=['period', 'save', 'units'], prog_name='plot_unem')
    if not save_state:
        save_state = False
    units = 'pc1' if units is None else units

    if isinstance(period, str):
        print(f"Fetching plot chart for Unemployment rate: % Change from Year Ago...")
        try:
            plot.plot_unemployment(period=period, save=save_state, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_unem -p 3M -s yes')

def plot_indp(arg):
    period, save_state, units = parse_args(arg_str=arg, expected_args=['period', 'save', 'units'], prog_name='plot_indp')
    if not save_state:
        save_state = False
    units = 'pc1' if units is None else units

    if isinstance(period, str):
        print(f"Fetching plot chart for Industrial Production: % Change from Year Ago...")
        try:
            plot.plot_ind_prod(period=period, save=save_state, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_indp -p 3M -s yes')

def plot_netex(arg):
    period, save_state, units = parse_args(arg_str=arg, expected_args=['period', 'save', 'units'], prog_name='plot_netex')
    if not save_state:
        save_state = False
    units = 'lin' if units is None else units

    if isinstance(period, str):
        print(f"Fetching plot chart for Real Net Exports of Goods and Services...")
        try:
            plot.plot_netex(period=period, save=save_state, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_netex -p 3M -s yes')

