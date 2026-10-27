from django.apps import AppConfig


class GduPilotoConfig(AppConfig):
    """Modelos managed=False del piloto visualizador-gdu (schemas catastro/our/
    visualizador/vistas/audit copiados del dump de Hasura). Transitorio: las vistas
    de gdu/ los siguen usando hasta que se re-apunten a los modelos propios de
    gdu.models; después esta app se elimina entera."""
    name = 'gdu_piloto'
