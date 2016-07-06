"""
Wrapper for loading templates from the TIM Tec themes.
"""

from django.conf import settings
from django.template.loaders.filesystem import Loader
from django.apps import apps
from django.utils._os import safe_join


class TimtecThemeLoader(Loader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        The template name shold be in format: theme_name:templatename.html
        The THEMES_DIR variable must be set in settings.py
        Usage example: {% extends "default:course.html" %}
        """
        if ':' in template_name:
            theme_name, template_name = template_name.split(":", 1)
            template_dirs = [safe_join(settings.THEMES_DIR, theme_name, 'templates')]

        # try to load template from theme app
        elif apps.is_installed(settings.TIMTEC_THEME):
            theme_app_config = apps.get_app_config(settings.TIMTEC_THEME)
            template_dirs = [theme_app_config.path]
        else:
            # LEGACY: try to load theme from themes dir
            template_dirs = [safe_join(settings.THEMES_DIR, settings.TIMTEC_THEME, 'templates')]

        template_dirs.append(safe_join(settings.THEMES_DIR, 'default', 'templates'))

        return super(TimtecThemeLoader, self).get_template_sources(template_name, template_dirs)
