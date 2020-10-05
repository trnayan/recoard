import logging

from django.conf import settings
from django.utils.module_loading import import_string


logger = logging.getLogger(__name__)


class MetadataPlugins:

    def __init__(self):
        self._plugins = []

        for plugin in settings.PAPERMERGE_METADATA_PLUGINS:
            self._plugins.append(
                import_string(plugin)
            )

    def __iter__(self):
        for plugin in self._plugins:
            yield plugin


def get_plugin_by_module_name(module_name):

    plugins = MetadataPlugins()

    for plugin in plugins:
        if plugin.__module__ == module_name:
            return plugin

    return None
