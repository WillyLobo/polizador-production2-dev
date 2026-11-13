"""Manda los modelos de `necesidades` a su propia base, si hay una configurada.

La base de desarrollo (polizadordbdev) se destruye y recrea seguido; los pedidos
que cargan los usuarios no se pueden perder con ella. Si el .env define
NECESIDADES_DATABASE_URL, settings.py agrega el alias "necesidades" y todo lo de
esta app se lee, escribe y migra ahí. Si no lo define (local, tests, o un
servidor cuya base no se recrea), todo queda en "default" como cualquier app.

Por eso los modelos no tienen ForeignKey a CustomUser: Django no permite
relaciones entre bases distintas. Se guarda el username y el nombre visible.

Ojo: los permisos y contenttypes de la app viven siempre en "default" (los crea
`migrate` sobre default), así que al recrear polizadordbdev hay que volver a
asignar `necesidades.gestionar_necesidad` a quien corresponda.
"""

from django.conf import settings

ALIAS = "necesidades"
APP_LABEL = "necesidades"


def alias_necesidades():
    return ALIAS if ALIAS in settings.DATABASES else "default"


class NecesidadesRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == APP_LABEL:
            return alias_necesidades()
        return None

    db_for_write = db_for_read

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == APP_LABEL and obj2._meta.app_label == APP_LABEL:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == APP_LABEL:
            return db == alias_necesidades()
        if db == ALIAS:
            # La base de necesidades solo tiene las tablas de esta app.
            return False
        return None
