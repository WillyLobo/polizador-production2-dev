from django.apps import AppConfig


class PersonalizadorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personalizador'
    verbose_name = 'Personal'

    def ready(self):
        import personalizador.history
