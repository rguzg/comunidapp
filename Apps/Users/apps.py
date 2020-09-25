from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'Apps.Users'

    def ready(self):
        import Apps.Users.signals