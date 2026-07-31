from django.conf import settings
from django.db import models


class UsuarioMigrado(models.Model):
    """
    Trazabilidad de la migración de visualizador.user -> settings.AUTH_USER_MODEL,
    corrida por gdu/management/commands/migrar_usuarios_gdu.py. A diferencia del
    resto de gdu/models/*, esta tabla es nueva y managed=True (no espeja nada
    de la base heredada).
    """
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="gdu_migracion",
    )
    visualizador_user_id = models.IntegerField(unique=True)
    area_nombre = models.CharField(max_length=255, blank=True)
    cuenta_reutilizada = models.BooleanField(
        default=False,
        help_text="True si ya existía un CustomUser con ese username y se reutilizó en vez de crear uno nuevo.",
    )
    migrado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} (visualizador.user #{self.visualizador_user_id})"


class ObraContratacion(models.Model):
    """
    Vínculo entre carga.Obra y catastro.contratacion, resuelto por
    gdu/management/commands/vincular_obras_contrataciones.py haciendo matching por
    expediente normalizado (gdu.matching.normalizar_expediente). Igual que
    UsuarioMigrado, tabla nueva y managed=True (no espeja nada de la base heredada).
    """
    obra = models.OneToOneField(
        "carga.Obra", on_delete=models.CASCADE, related_name="gdu_contratacion",
    )
    contratacion = models.ForeignKey(
        "Contratacion", on_delete=models.PROTECT, related_name="obras_vinculadas",
    )
    vinculado_manualmente = models.BooleanField(
        default=False,
        help_text="True si el vínculo vino de una corrección manual (--csv-correcciones) en vez de un match automático único.",
    )
    vinculado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Obra #{self.obra_id} <-> Contratación #{self.contratacion_id}"
