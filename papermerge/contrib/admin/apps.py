from django.apps import AppConfig, apps
from .registries import user_menu_registry


class AdminConfig(AppConfig):
    name = 'papermerge.contrib.admin'

    def ready(self):
        from papermerge.contrib.admin import signals  # noqa

        # autodiscover user menu items from user_menu.py modules
        app_names = [app.name for app in apps.app_configs.values()]
        user_menu_registry.autodiscover(app_names)
