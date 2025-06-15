from qemy.data.api_fred import FREDData
from qemy.utils.parse_arg import parse_args

#================================== FRED =====================================#

def rfr():
    try:
        print(FREDData().get_tbill_yield())
    except Exception as e:
        print(f"Could not fetch data ERROR:\n{e}")

def cpi(arg):
    period, units = parse_args(arg_str=arg, expected_args=['period', 'units'], prog_name='cpi')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(FREDData().get_cpi(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: cpi -p 1Y')

def gdp(arg):
    period, units = parse_args(arg_str=arg, expected_args=['period', 'units'], prog_name='gdp')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(FREDData().get_gdp(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: gdp -p 1Y')

def sent(arg):
    period, units = parse_args(arg_str=arg, expected_args=['period', 'units'], prog_name='sent')
    units = 'pch' if units is None else units
    if isinstance(period, str):
        try:
            print(FREDData().get_sentiment(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: sent -p 1Y')

def nfp(arg):
    period, units = parse_args(arg_str=arg, expected_args=['period', 'units'], prog_name='nfp')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(FREDData().get_nf_payrolls(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: nfp -p 1Y')

def interest(arg):
    period, units = parse_args(arg_str=arg, expected_args=['period', 'units'], prog_name='interest')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(FREDData().get_interest_rate(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: interest -p 1Y')

def jobc(arg):
    period, units = parse_args(arg_str=arg, expected_args=['period', 'units'], prog_name='jobc')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(FREDData().get_jobless_claims(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: jobc -p 1Y')

def unem(arg):
    period, units = parse_args(arg_str=arg, expected_args=['period', 'units'], prog_name='unem')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(FREDData().get_unemployment(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: unem -p 1Y')

def indp(arg):
    period, units = parse_args(arg_str=arg, expected_args=['period', 'units'], prog_name='indp')
    units = 'pc1' if units is None else units
    if isinstance(period, str):
        try:
            print(FREDData().get_industrial_production(period=period, units=units))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: indp -p 1Y')

def netex(arg):
    period, units = parse_args(arg_str=arg, expected_args=['period', 'units'], prog_name='netex')
    units = 'lin' if units is None else units 
    if isinstance(period, str) and isinstance(units, str):
        try:
            print(FREDData().get_net_exports(period=period, units=units.lower()))
        except Exception as e:
            print(f"Could not fetch data ERROR:\n{e}")
    else:
        print('For valid syntax, Try: netex -p 1Y')

