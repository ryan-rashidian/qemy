""""""

import importlib.util
from pathlib import Path

class PluginRegistry:
    """"""
    def __init__(self):
        """"""
        self.models = {}

    def register_model(self, name, func):
        """"""
        self.models[name] = func

def load_plugins(plugin_dir="plugins"):
    """"""
    registry = PluginRegistry()
    base_path = Path(__file__).parent.parent / plugin_dir

    found_plugins = False

    for plugin_folder in base_path.iterdir():
        if plugin_folder.is_dir():
            plugin_file = plugin_folder / "plugin.py"
            if plugin_file.exists():
                spec = importlib.util.spec_from_file_location(
                    plugin_folder.name, plugin_file
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, "register"):
                        module.register(registry)
                        found_plugins = True

    if not found_plugins:
        print("No plugins found.")

    return registry
