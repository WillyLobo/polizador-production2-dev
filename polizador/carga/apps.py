from django.apps import AppConfig


class CargaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carga'
    verbose_name = 'Obras'

    def ready(self):
        import carga.signals
        import carga.history
