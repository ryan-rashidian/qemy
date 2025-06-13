from qemy.core.models.dcf import get_dcf_eval
from qemy.core.models.linear_r import linear_r
from qemy.core.models.monte_carlo import monte_carlo_sim
from qemy.core.plugin_loader import load_plugins
from qemy.core.plot.plot import plot_models
from qemy.utils.parse_arg import parse_args

# test block
def run_models(arg):
    period, ticker, model, num, plot, save = parse_args(
        arg_str=arg, 
        expected_args=['period', 'ticker', 'model', 'num', 'plot', 'save'], 
        prog_name='run_model'
    )
    if isinstance(save, str) and save.lower() == 'yes':
        save = True
    else:
        save = False
    arg_dict = {
        'ticker': ticker,
        'period': period,
        'num': num,
    }

    try:
        registry = load_plugins()
        model_func = registry.models.get(model)
        if model_func:
            results = model_func(**arg_dict)
            if not isinstance(results, dict):
                print("Plugin failed to return results")
                return

            if "text" in results:
                print("\nPlugin Results:")
                for key, value in results["text"].items():
                    if isinstance(value, (int, float)):
                        print(f"{key}: {value:.4f}")
                    else:
                        print(f"{key}: {value}")

            if "plot" in results and plot:
                plot_data = results["plot"]
                print("Launching plot")
                plot_models(
                    ticker = ticker, 
                    x_axis = plot_data.get("x_axis"), 
                    y_axis = plot_data.get("y_axis"), 
                    title = plot_data.get("title"),
                    plot= plot,
                    save = save
                )

        else:
            print(f"Model '{model}' not found.")
    except Exception as e:
        print(f"Error in cli_model.py:\n{e}")
## test block

def dcf(arg):
    get_dcf_eval(arg)

def lr(arg):
    period, ticker = parse_args(arg_str=arg, expected_args=['period', 'ticker'], prog_name='linear_r')
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
    period, ticker, num = parse_args(arg_str=arg, expected_args=['period', 'ticker', 'num'], prog_name='mcarlo')
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

