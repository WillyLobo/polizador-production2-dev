from django.core.management.base import BaseCommand
from django.db import transaction
from secretariador.models import ComisionadoSolicitud

# Relaciones que get_origin()/valor_viatico_dia() recorren en cada save():
# precargarlas evita N+1 queries sobre Solicitud/Incorporacion/Agente.
SELECT_RELATED = (
    "comisionadosolicitud_foreign__solicitud_decreto_viaticos",
    "comisionadosolicitud_foreign__solicitud_provincia",
    "comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud__solicitud_decreto_viaticos",
    "comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud__solicitud_provincia",
    "comisionadosolicitud_nombre",
)
PREFETCH_RELATED = ("comisionadosolicitud_nombre__directorio_set",)


class Command(BaseCommand):
    """
    Management command: recorre todos los ComisionadoSolicitud y los
    vuelve a guardar, para forzar el recalculo de los campos derivados
    (dias, viatico diario, viatico computado, viatico total) definidos
    en ComisionadoSolicitud.save().

    Uso: python manage.py resave_comisionado
    """

    def handle(self, *args, **kwargs):
        queryset = ComisionadoSolicitud.objects.select_related(
            *SELECT_RELATED
        ).prefetch_related(*PREFETCH_RELATED)
        total = queryset.count()
        self.stdout.write(f"Se encontraron {total} ComisionadoSolicitud")

        guardados = 0
        errores = 0

        with transaction.atomic():
            for comisionado in queryset.iterator(chunk_size=500):
                try:
                    comisionado.save()
                    guardados += 1
                except Exception as e:
                    errores += 1
                    self.stderr.write(
                        self.style.ERROR(
                            f"Error al guardar ComisionadoSolicitud {comisionado.pk}: {e}"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nResumen: {guardados} guardado(s), {errores} error(es)"
            )
        )
