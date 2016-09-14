from django.apps import AppConfig


class ActivitiesConfig(AppConfig):
    name = 'activities'
    verbose_name = 'Activities'

    def ready(self):
        import activities.signals
