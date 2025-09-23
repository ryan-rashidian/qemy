"""PLACEHOLDER: Plugin loader for Qemy CLI."""

from collections.abc import Callable

from qemy.config.paths import PLUGINS_DIR


class PluginRegistry:
    """Central plugin registry."""

    def __init__(self):
        """"""
        self.plugins: dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> None:
        """"""
        self.plugins[name] = func

def load_plugins() -> PluginRegistry:
    """Placeholder"""
    registry = PluginRegistry()
    base_path = PLUGINS_DIR

    if not base_path:
        return registry

    return registry

