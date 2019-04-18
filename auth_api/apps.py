from django.apps import AppConfig

class AuthApiConfig(AppConfig):
    name = 'auth_api'


    def ready(self):
        import auth_api.signals
