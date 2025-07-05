"""Plugin loader for Qemy CLI."""

import importlib.util
from collections.abc import Callable
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class PluginRegistry:
    """Central plugin registry."""

    def __init__(self):
        """Initialize registry."""
        self.models = {}

    def register_model(self, name: str, func: Callable) -> None:
        """Add a plugin to the registry."""
        self.models[name] = func

def load_plugins() -> PluginRegistry:
    """Dynamically discovers and loads all plugin modules.

    Searches subfolders in /plugins/
    Loads plugin modules into 'registry' PluginRegistry object

    Returns: 
        registry (PluginRegistry): Contains all discovered plugins
    """
    registry = PluginRegistry()
    base_path = Path(__file__).parent

    found_plugins = False

    for plugin_folder in base_path.iterdir():
        if plugin_folder.is_dir():
            plugin_file = plugin_folder / "plugin.py"

            if plugin_file.exists():
                # Create module spec
                spec = importlib.util.spec_from_file_location(
                    plugin_folder.name, plugin_file
                )

                if spec and spec.loader:
                    # Create empty module object from spec
                    module = importlib.util.module_from_spec(spec)
                    # Execute plugin.py inside module
                    spec.loader.exec_module(module)

                    if hasattr(module, "register"):
                        # Call register() if it exists
                        module.register(registry)
                        found_plugins = True
                        logger.debug(f"{plugin_folder.name} loaded")

    if not found_plugins:
        logger.warning("No plugins found")

    return registry

