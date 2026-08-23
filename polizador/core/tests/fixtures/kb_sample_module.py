"""Fixture para core/tests/test_knowledge_base_extract.py.

Nunca se importa: el test solo lee este archivo como texto y lo copia a un directorio de
app temporal, para ejercitar el extractor ast (`core/knowledge_base.py`) sin tocar la app
`carga` real.
"""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Widget(models.Model):
    """Un widget de prueba."""

    nombre = models.CharField(max_length=100)

    def etiqueta(self) -> str:
        """Devuelve el nombre en mayúsculas."""
        return self.nombre.upper()


def crear_widget(nombre):
    """Crea un Widget a partir de un nombre."""
    return Widget.objects.create(nombre=nombre)


@receiver(post_save, sender=Widget)
def widget_creado(sender, instance, created, **kwargs):
    """Se dispara al guardar un Widget."""
    pass
