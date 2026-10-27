from django.conf import settings
from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords

# Todas las geometrías de GDU se guardan en POSGAR 2007 faja 5, como en la base heredada.
SRID_GDU = 22175


class Auditado(models.Model):
    """Reemplaza al trigger set_updated() de la base heredada, que guardaba el rol de
    Postgres (current_user) en vez del usuario real. updated_by lo setea quien escribe
    (formularios, admin, OAPIF save_model); el historial completo queda en history."""
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True, editable=False, related_name="+",
    )
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class Lookup(Auditado):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        abstract = True
        ordering = ["nombre"]


class EstadoDominial(models.TextChoices):
    # unión de los enums heredados parcela_estado_dominial (vivienda_punto) y
    # parcela_estado_dominial_2 (parcela, uf)
    PROPIETARIO = "propietario", "Propietario"
    IPDUV = "ipduv", "IPDUV"
    ADJUDICATARIO = "adjudicatario", "Adjudicatario"
    MUNICIPIO = "municipio", "Municipio"
    ESTADO_PROVINCIAL = "estado_provincial", "Estado Provincial"
    ESTADO_NACIONAL = "estado_nacional", "Estado Nacional"
    ESTADO_MUNICIPAL = "estado_municipal", "Estado Municipal"
    PRIVADO = "privado", "Privado"
    DONADO = "donado", "Donado"
    VERIFICAR = "verificar", "Verificar"


class TipoResolucion(models.TextChoices):
    PROVISORIA = "provisoria", "Provisoria"
    DEFINITIVA = "definitiva", "Definitiva"


_PARTES_NOMENCLATURA = [
    ("dpto", 2, "Departamento"),
    ("circ", 3, "Circunscripción"),
    ("secc", 2, "Sección"),
    ("ch", 4, "Chacra"),
    ("qta", 4, "Quinta"),
    ("fracc", 4, "Fracción"),
    ("mz", 4, "Manzana"),
    ("parc", 5, "Parcela"),
]


def _nomenclatura_abstracta(obligatoria):
    """Las 8 partes de la nomenclatura catastral + la nomenclatura completa como
    GeneratedField (reemplaza al trigger set_nomenclatura(); vale también para lo que
    se escriba por fuera del ORM). Mismo criterio que el trigger: `||` devuelve NULL
    si falta alguna parte."""
    opcional = {} if obligatoria else {"blank": True, "null": True}
    atributos = {
        nombre: models.CharField(verbose_name, max_length=largo, **opcional)
        for nombre, largo, verbose_name in _PARTES_NOMENCLATURA
    }
    atributos["nomenclatura"] = models.GeneratedField(
        expression=models.Func(
            *[models.F(nombre) for nombre, _, _ in _PARTES_NOMENCLATURA],
            template="(%(expressions)s)",
            arg_joiner=" || ",
        ),
        output_field=models.CharField(max_length=28, null=True),
        db_persist=True,
    )
    atributos["Meta"] = type("Meta", (), {"abstract": True})
    atributos["__module__"] = __name__
    nombre_clase = "NomenclaturaCatastral" if obligatoria else "NomenclaturaCatastralOpcional"
    return type(nombre_clase, (models.Model,), atributos)


NomenclaturaCatastral = _nomenclatura_abstracta(obligatoria=True)
NomenclaturaCatastralOpcional = _nomenclatura_abstracta(obligatoria=False)
