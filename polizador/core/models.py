from django.conf import settings
from django.db import models
from django.utils import timezone


class ManagementCommandRun(models.Model):
    class Status(models.TextChoices):
        RUNNING = "running", "En ejecución"
        SUCCESS = "success", "Éxito"
        FAILED = "failed", "Falló"
        KILLED = "killed", "Detenido"

    STATUS_BADGE = {
        Status.RUNNING: "primary",
        Status.SUCCESS: "success",
        Status.FAILED: "danger",
        Status.KILLED: "secondary",
    }

    class Meta:
        verbose_name = "Ejecución de comando"
        verbose_name_plural = "Ejecuciones de comandos"
        ordering = ("-started_at",)

    # Clave dentro de core.management_commands_registry.COMMAND_REGISTRY, no el
    # nombre del management command en si (el whitelist es la unica fuente de
    # verdad sobre que se puede ejecutar desde la web).
    command = models.CharField(max_length=100)
    argv = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.RUNNING)
    started_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="management_command_runs"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    return_code = models.IntegerField(null=True, blank=True)
    pid = models.IntegerField(null=True, blank=True)
    log = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.command} @ {self.started_at:%Y-%m-%d %H:%M}"

    @property
    def label(self):
        from core.management_commands_registry import COMMAND_REGISTRY

        meta = COMMAND_REGISTRY.get(self.command)
        return meta["label"] if meta else self.command

    @property
    def status_badge(self):
        return self.STATUS_BADGE.get(self.status, "secondary")

    @property
    def duration(self):
        """Tiempo transcurrido como timedelta. Mientras status==RUNNING, se calcula
        contra "ahora" (aproximado: crece en cada request, no es un valor fijo)."""
        end = self.finished_at or (timezone.now() if self.status == self.Status.RUNNING else None)
        if end is None:
            return None
        return end - self.started_at

    @property
    def duration_display(self):
        duration = self.duration
        if duration is None:
            return "—"
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}h {minutes}m {seconds}s"
        if minutes:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"


class Todo(models.Model):
    class Status(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        PARCIAL = "parcial", "Parcialmente implementado"
        RESUELTO = "resuelto", "Resuelto"

    STATUS_BADGE = {
        Status.PENDIENTE: "secondary",
        Status.PARCIAL: "warning",
        Status.RESUELTO: "success",
    }

    class Meta:
        verbose_name = "Tarea pendiente"
        verbose_name_plural = "Tareas pendientes"
        ordering = ("status", "-updated_at")

    title = models.CharField("Título", max_length=200)
    description = models.TextField("Descripción", blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDIENTE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="todos_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def status_badge(self):
        return self.STATUS_BADGE.get(self.status, "secondary")


class FormValidationError(models.Model):
    class Meta:
        verbose_name = "Error de validación de formulario"
        verbose_name_plural = "Errores de validación de formularios"
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["created_at"]), models.Index(fields=["view_name"])]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="form_validation_errors",
    )
    path = models.CharField(max_length=500)
    view_name = models.CharField(max_length=255)
    form_class_path = models.CharField(max_length=255, blank=True, default="")
    """Dotted path para re-importar la clase del form con import_string. Vacio si la
    clase es dinamica (ej. build_matriz_form) y no tiene path estable."""
    form_errors = models.JSONField(default=dict, blank=True)
    formsets = models.JSONField(default=list, blank=True)
    """[{"prefix": str, "class_path": str, "errors": [...]}, ...]"""
    raw_data = models.JSONField(default=dict, blank=True)
    """{field_name: [valores...]} - siempre listas para soportar campos multivaluados."""
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.view_name} @ {self.created_at:%Y-%m-%d %H:%M}"


class LoginEvent(models.Model):
    class Meta:
        verbose_name = "Inicio de sesión"
        verbose_name_plural = "Inicios de sesión"
        ordering = ("-timestamp",)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="login_events")
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} @ {self.timestamp:%Y-%m-%d %H:%M}"
