from django.db import models


class ObraContratacion(models.Model):
    """
    Vínculo entre carga.Obra y catastro.contratacion, resuelto por
    gdu/management/commands/vincular_obras_contrataciones.py haciendo matching por
    expediente normalizado (gdu.matching.normalizar_expediente). A diferencia del
    resto de gdu/models/*, esta tabla es nueva y managed=True (no espeja nada de
    la base heredada).
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
