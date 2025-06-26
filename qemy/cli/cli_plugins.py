from qemy.core.plugin_loader import load_plugins
from qemy.core.plot.plot import plot_models
from qemy.utils.parse_arg import parse_args_cli, check_help
from qemy.cli.cli_helper import print_help_table

def run_models(arg):
    if check_help(
        arg_str=arg,
        help_func=lambda: print_help_table(" m ", [
            ("Info:", "Loads a given plugin"),
            ("Usage:", "m <plugin>\n"),
        ])
    ):
        return

    core_args, plugin_kwargs, other_args = parse_args_cli(
        arg_str=arg, 
        expected_args=[
            'period', 'ticker_flag', 'model',
            'num', 'plot', 'save', 'help'
        ], 
        prog_name='run_model'
    )

    if other_args:
        print(f"Unexpected Command: {other_args}")

    period, ticker, model, num, plot, save, help = core_args

    if not save:
        save = False
    arg_dict = {
        'ticker': ticker,
        'period': period,
        'num': num,
    }

    try:
        registry = load_plugins()
        model_cls = registry.models.get(model)
        if model_cls:
            print(f"\n[Plugin: {model_cls.name}]")
            print(f"{model_cls.description} (v{model_cls.version})")
            plugin_instance = model_cls(**arg_dict, **plugin_kwargs)

            if help:
                print(plugin_instance.help())
                return

            results = plugin_instance.run()
            if not isinstance(results, dict):
                print("\nPlugin failed to return results")
                return

            if "text" in results:
                print("\nPlugin Results:")
                for key, value in results["text"].items():
                    print(f"{key}: {value}")

            if "plot" in results and plot:
                plot_data = results["plot"]
                print("Launching plot")
                plot_models(
                    title = plot_data.get("title"),
                    plot_func = plot_data.get("plot_func"),
                    save = save
                )

        else:
            print(f"Model '{model}' not found.")
    except Exception as e:
        print(f"Error in cli_model.py:\n{e}")

