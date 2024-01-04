from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'accounts'
    def ready(self):
        import accounts.signals
