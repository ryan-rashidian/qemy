from qemy.core.plugin_loader import load_plugins
from qemy.core.plot.plot import plot_models
from qemy.utils.parse_arg import parse_args

def run_models(arg):
    period, ticker, model, num, plot, save = parse_args(
        arg_str=arg, 
        expected_args=['period', 'ticker_flag', 'model', 'num', 'plot', 'save'], 
        prog_name='run_model'
    )
    if not save:
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
                    title = plot_data.get("title"),
                    plot_func = plot_data.get("plot_func"),
                    save = save
                )

        else:
            print(f"Model '{model}' not found.")
    except Exception as e:
        print(f"Error in cli_model.py:\n{e}")

