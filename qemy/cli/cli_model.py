from qemy.core.models.dcf import get_dcf_eval
from qemy.core.models.linear_r import linear_r
from qemy.core.models.monte_carlo import monte_carlo_sim
from qemy.utils import parse_arg
from qemy.core.plugin_loader import load_plugins

# test block
def run_models(arg, model="linear_r"):
    period, ticker = parse_arg.parse_arg_p_t(arg=arg, name='plot_lr')
    if isinstance(period, str) and isinstance(ticker, str):
        try:
            registry = load_plugins()
            model_func = registry.models.get(model)
            if model_func:
                results = model_func(ticker, period)
                if isinstance(results, dict):
                    print("\nPlugin Results:")
                    for key, value in results.items():
                        print(f"{key}: {value:.4f}")
                else:
                    print("Plugin failed to return results")
            else:
                print(f"Model '{model}' not found.")
        except Exception as e:
            print(f"Error in cli_model.py:\n{e}")
    else:
        print("Placeholder")
## test block

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

