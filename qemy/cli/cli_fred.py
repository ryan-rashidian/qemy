from qemy.data import api_fred as fred
from qemy.utils import parse_arg
#=============================================================================#
################################## FRED #######################################
#=============================================================================#
def rfr():
    try:
        print(fred.get_tbill_yield())
    except Exception as e:
        print(f"Could not fetch data ERROR:\n{e}")
#=============================================================================#
def cpi(arg):
    period, units = parse_arg.parse_arg_p_u(arg=arg, name='cpi')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(fred.get_cpi_inflation(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: cpi -p 1Y')
#=============================================================================#
def gdp(arg):
    period, units = parse_arg.parse_arg_p_u(arg=arg, name='gdp')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(fred.get_gdp(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: gdp -p 1Y')
#=============================================================================#
def sent(arg):
    period, units = parse_arg.parse_arg_p_u(arg=arg, name='sent')
    units = 'pch' if units is None else units
    if isinstance(period, str):
        try:
            print(fred.get_sentiment(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: sent -p 1Y')
#=============================================================================#
def nfp(arg):
    period, units = parse_arg.parse_arg_p_u(arg=arg, name='nfp')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(fred.get_nf_payrolls(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: nfp -p 1Y')
#=============================================================================#
def interest(arg):
    period, units = parse_arg.parse_arg_p_u(arg=arg, name='interest')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(fred.get_interest(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: interest -p 1Y')
#=============================================================================#
def jobc(arg):
    period, units = parse_arg.parse_arg_p_u(arg=arg, name='jobc')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(fred.get_jobless_claims(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: jobc -p 1Y')
#=============================================================================#
def unem(arg):
    period, units = parse_arg.parse_arg_p_u(arg=arg, name='unem')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(fred.get_unemployment(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: unem -p 1Y')
#=============================================================================#
def indp(arg):
    period, units = parse_arg.parse_arg_p_u(arg=arg, name='indp')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(fred.get_ind_prod(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: indp -p 1Y')
#=============================================================================#
def netex(arg):
    period, units = parse_arg.parse_arg_p_u(arg=arg, name='netex')
    units = 'lin' if units is None else units 
    if isinstance(period, str) and isinstance(units, str):
        try:
            print(fred.get_netex(period=period, units=units.lower()))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: netex -p 1Y')

