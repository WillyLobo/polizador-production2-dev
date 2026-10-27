from django.conf import settings
from django.contrib.gis.db import models
from django.utils import timezone


class EventoVisor(models.Model):
    """Actividad de los usuarios en el visor (login, descarga de planos, impresiones).
    Los eventos nuevos se registran del lado del servidor con request.user; los
    importados de audit.audit_logs quedan con importado=True y, si el usuario no se
    pudo resolver, solo con username."""
    tstamp = models.DateTimeField(default=timezone.now, db_index=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True, related_name="+")
    username = models.CharField(max_length=255, blank=True)
    accion = models.CharField("acción", max_length=255)
    ip = models.GenericIPAddressField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    importado = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"{self.username} - {self.accion} ({self.tstamp:%d/%m/%Y %H:%M})"

    class Meta:
        verbose_name = "evento del visor"
        verbose_name_plural = "eventos del visor"
        ordering = ["-tstamp"]
