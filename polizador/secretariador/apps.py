from django.apps import AppConfig


class SecretariadorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'secretariador'
    verbose_name = 'Viáticos'

    def ready(self):
        import secretariador.signals
        import secretariador.history
