# Contributing to Qemy

Thank you for your interest in contributing to **Qemy**, This document will help you build your own plugin or improve the core project.

## Creating a Plugin 

Qemy uses a modular plugin system to extend its functionality. Each plugin should follow a consistent structure so it can be loaded and run within the CLI seamlessly.

Prerequisites:
- Qemy installed in [development mode](docs/dev_setup.md).

Tip: Reference existing plugins to supplement this guide

### Directory Structure

Create a folder for your plugin in: qemy/plugins/

In your plugin folder, create 3 files:
- `__init__.py` # can remain empty
- `plugin.py` 
- `your_plugin.py`

### Plugin Structure

Qemy plugins use a parent class BasePlugin located at qemy/core/plugin_base.py

#### `your_plugin.py`

In `your_plugin.py`:
- Create a class that inherits from BasePlugin
- Define a name, description, and version
- Implement a run(self) method

```python
from qemy.core.plugin_base import BasePlugin

class YourPlugin(BasePlugin):
    name = "example"
    description = "This plugin is for ..."
    version = "0.1.0"

    def run(self):
```

In run(self) method:
- Return your plugins CLI output in nested dictionary
- Expects a "text" and/or "plot" key
- Each key/value pair within the nested dictionary under "text" key will be printed out in the CLI sequentially.
- "plot" key also expects a nested dictionary with "title" and "plot_func" keys
- Use the following as a recommended template:

```python
    def run(self):
        ... ### Your code here
        return {
            "text": {
                "Subject:": f"{subject}",
                "Result:": f"{result:.2f}"
            },
            "plot": {
                "title": "Plugin Plot Title",
                "plot_func": lambda: (
                    ... # matplotlib.pyplot.plot()
                )
            }
        }
```

Write a help(self) method for YourPlugin:
- The help(self) method expects a string object as the return 
- Use the following as a recommended template:

```python
    def help(self):
        return (
            f"{self.name.upper()} Plugin Help:\n"
            f"Description: {self.description}\n"
            f"Version: {self.version}\n\n"
            f"Info about your plugin here."
        )
```

Call inherited self.log() method:
- Recommended for debugging
- For example:

```python
    def run(self):
        try:
            ... # Your code here
            return {"text": {"Example:": f"{example}"}}

        except Exception as e:
            self.log(f"YourPlugin Error:\n{e}")
```

#### `plugin.py`

In `plugin.py`: 
- Define a register() function
- Import YourPlugin
- Register YourPlugin
- Use the following as a recommended template:

```python
def register(registry):
    from qemy.plugins.your_folder.your_plugin import YourPlugin
    registry.register_model(YourPlugin.name, YourPlugin)
```

### Plugin Syntax

BasePlugin parent class defines instance variables that correspond with CLI arguments:
- -t --ticker -> self.ticker
- -p --period -> self.period
- -n --num    -> self.num

You can define custom, plugin specific CLI arguments using the self.args instance variable:

```python
custom_arg = self.args.get('example', None) 
# or 
custom_arg = self.args.get('example', False)
```

- When a flagged argument (using 2 dashes as a prefix: '--') is given in the CLI, and does not match any existing core arguments, it will automatically be assigned to the self.args variable inside a dictionary
- Within that dictionary, flagged arguments are split into key/value pairs. For example:

```bash
--flag custom
# or 
--flag
```

Entered into the CLI, becomes:

```python
self.args = {'flag', 'custom'}
# or
self.args = {'flag', True}
```

- Note: Custom arguments return a string, or boolean, depending on whether a undefined, white-space defined token follows the --flag itself
- Tip: Add a print statement explaining any custom arguments in your plugin to your help(self) method

### Qemy SDK

**Work in Progress**

- matplotlib is integrated through the "plot" dictionary key and its nested "plot_func" key - which should hold a function performing a pyplot.plot() as its value (example shown above)
- scikit-learn, numpy and pandas libraries are available in the Qemy Python environment for your plugin as well
- For now, please reference modules in qemy/data/ or use existing plugins as examples for how to use the core codebase of Qemy to build your plugin. A full guide will be made after the foundation of the SDK is complete due to ongoing changes. Thank you for your interest!

