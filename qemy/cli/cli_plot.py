from plot import plot
from utils import parse_arg
#=============================================================================#
################################## PLOT #######################################
#=============================================================================#
def plot_price(arg):
    period, ticker = parse_arg.parse_arg_p_t(arg=arg, name='plot_price')
    if isinstance(period, str) and isinstance(ticker, str):
        print(f"Fetching plot chart for: {ticker} daily closing prices, log scaled...")
        try:
            plot.plot_price(ticker=ticker, period=period)
        except Exception as e:
            print(f"Could not fetch plot chart, please try another ticker. Error:\n{e}")
    else:
        print('For valid syntax, Try: plot_price AAPL -p 3M')
#=============================================================================#
def plot_lr(arg):
    period, ticker = parse_arg.parse_arg_p_t(arg=arg, name='plot_lr')
    if isinstance(period, str) and isinstance(ticker, str):
        print(f"Fetching plot chart for: {ticker} daily closing prices...")
        try:
            plot.plot_lr(ticker=ticker, period=period)
        except Exception as e:
            print(f"Could not fetch plot chart, please try another ticker. Error:\n{e}")
    else:
        print('For valid syntax, Try: price_plot AAPL -p 3M')
#=============================================================================#
def plot_monte_carlo(arg):
    period, ticker, num = parse_arg.parse_arg_p_t_n(arg=arg, name='plot_montec')
    if isinstance(period, str) and isinstance(ticker, str) and num:
        num = int(num)
        try:
            plot.plot_monte_carlo(ticker=ticker, period=period, num_simulations=num)
        except Exception as e:
            print(f"Error:\n{e}")
    else:
        print('For valid syntax, Try: monte_carlo -p 2Y -n 1000')
#=============================================================================#
def plot_cpi(arg):
    period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_cpi')
    units = 'pc1' if units is None else units
    if isinstance(period, str) and isinstance(save_state, str):
        print(f"Fetching plot chart for CPI inflation: % Change from Year Ago...")
        try:
            if save_state in ('Y', 'YES'):
                plot.plot_cpi(period=period, save=True, units=units)
            else:
                plot.plot_cpi(period=period, save=False, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_cpi -p 3m -s yes')
#=============================================================================#
def plot_gdp(arg):
    period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_gdp')
    units = 'pc1' if units is None else units
    if isinstance(period, str) and isinstance(save_state, str):
        print(f"Fetching plot chart for GDP: % Change from Year Ago...")
        try:
            if save_state in ('Y', 'YES'):
                plot.plot_gdp(period=period, save=True, units=units)
            else:
                plot.plot_gdp(period=period, save=False, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_gdp -p 3M -s yes')
#=============================================================================#
def plot_sent(arg):
    period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_sent')
    units = 'pch' if units is None else units
    if isinstance(period, str) and isinstance(save_state, str):
        print(f"Fetching plot chart for Sentiment: % Change...")
        try:
            if save_state in ('Y', 'YES'):
                plot.plot_sentiment(period=period, save=True, units=units)
            else:
                plot.plot_sentiment(period=period, save=False, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_sent -p 3M -s yes')
#=============================================================================#
def plot_nfp(arg):
    period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_nfp')
    units = 'pc1' if units is None else units
    if isinstance(period, str) and isinstance(save_state, str):
        print(f"Fetching plot chart for Non-Farm Payrolls: % Change from Year Ago...")
        try:
            if save_state in ('Y', 'YES'):
                plot.plot_nfp(period=period, save=True, units=units)
            else:
                plot.plot_nfp(period=period, save=False, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_nfp -p 3M -s yes')
#=============================================================================#
def plot_interest(arg):
    period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_interest')
    units = 'pc1' if units is None else units
    if isinstance(period, str) and isinstance(save_state, str):
        print(f"Fetching plot chart for Interest rates: % Change from Year Ago...")
        try:
            if save_state in ('Y', 'YES'):
                plot.plot_interest(period=period, save=True, units=units)
            else:
                plot.plot_interest(period=period, save=False, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_interest -p 3M -s yes')
#=============================================================================#
def plot_jobc(arg):
    period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_jobc')
    units = 'pc1' if units is None else units
    if isinstance(period, str) and isinstance(save_state, str):
        print(f"Fetching plot chart for Jobless Claims: % Change from Year Ago...")
        try:
            if save_state in ('Y', 'YES'):
                plot.plot_jobc(period=period, save=True, units=units)
            else:
                plot.plot_jobc(period=period, save=False, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_jobc -p 3M -s yes')
#=============================================================================#
def plot_unem(arg):
    period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_unem')
    units = 'pc1' if units is None else units
    if isinstance(period, str) and isinstance(save_state, str):
        print(f"Fetching plot chart for Unemployment rate: % Change from Year Ago...")
        try:
            if save_state in ('Y', 'YES'):
                plot.plot_unemployment(period=period, save=True, units=units)
            else:
                plot.plot_unemployment(period=period, save=False, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_unem -p 3M -s yes')
#=============================================================================#
def plot_indp(arg):
    period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_indp')
    units = 'pc1' if units is None else units
    if isinstance(period, str) and isinstance(save_state, str):
        print(f"Fetching plot chart for Industrial Production: % Change from Year Ago...")
        try:
            if save_state in ('Y', 'YES'):
                plot.plot_ind_prod(period=period, save=True, units=units)
            else:
                plot.plot_ind_prod(period=period, save=False, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_indp -p 3M -s yes')
#=============================================================================#
def plot_netex(arg):
    period, save_state, units = parse_arg.parse_arg_p_s_u(arg=arg, name='plot_netex')
    units = 'lin' if units is None else units
    if isinstance(period, str) and isinstance(save_state, str):
        print(f"Fetching plot chart for Real Net Exports of Goods and Services...")
        try:
            if save_state in ('Y', 'YES'):
                plot.plot_netex(period=period, save=True, units=units)
            else:
                plot.plot_netex(period=period, save=False, units=units)
        except Exception as e:
            print(f"Could not fetch plot chart. ERROR:\n{e}")
    else:
        print('For valid syntax, Try: plot_netex -p 3M -s yes')

