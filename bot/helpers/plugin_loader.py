import importlib
import pkgutil

from bot.config import DISABLED_PLUGINS
from bot.core.base_plugin import BasePlugin

DISABLED_PLUGINS.extend([])


def discover_plugins(plugins_package):
    
    plugin_classes = []

    for finder, name, ispkg in pkgutil.iter_modules(plugins_package.__path__):
        full_module_name = f"{plugins_package.__name__}.{name}"
        module = importlib.import_module(full_module_name)

        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if (
                    isinstance(attribute, type)
                    and issubclass(attribute, BasePlugin)
                    and attribute is not BasePlugin
            ):
                # Skip if class name is in DISABLED_PLUGINS
                if attribute.__name__ in DISABLED_PLUGINS:
                    continue
                plugin_classes.append(attribute)
    return plugin_classes
