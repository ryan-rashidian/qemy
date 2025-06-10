from qemy.core.models.dcf import get_dcf_eval
from qemy.core.models.linear_r import linear_r
from qemy.core.models.monte_carlo import monte_carlo_sim
from qemy.utils import parse_arg

def dcf(arg):
    get_dcf_eval(arg)

def lr(arg):
    period, ticker = parse_arg.parse_arg_p_t(arg=arg, name='plot_lr')
    if isinstance(period, str) and isinstance(ticker, str):
        try:
            _, _, alpha, beta, _ = linear_r(ticker=ticker, period=period)
            print(f"Alpha: {alpha:.6f}")
            print(f"Beta: {beta:.4f}")
        except Exception as e:
            print(f"Error:\n{e}")
    else:
        print('For valid syntax, Try: lr AAPL -p 1Y')
    
def monte_carlo(arg):
    period, ticker, num = parse_arg.parse_arg_p_t_n(arg=arg, name='monte_carlo')
    if isinstance(period, str) and isinstance(ticker, str) and num:
        try:
            num = int(num)
            _, end_mean, end_std, start_price = monte_carlo_sim(ticker=ticker, period=period, num_simulations=num)
            print(f"Start price:   {start_price:.2f}")
            print(f"End mean:      {end_mean:.2f}")
            print(f"End std:       {end_std:.4f}")
        except Exception as e:
            print(f"Error:\n{e}")
    else:
        print('For valid syntax, Try: monte_carlo -p 2Y -n 1000')

