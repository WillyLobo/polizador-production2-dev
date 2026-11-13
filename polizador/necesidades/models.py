from django.db import models


class Necesidad(models.Model):
    class Modulo(models.TextChoices):
        VISOR = "visor", "GDU: visor / mapa web"
        FICHAS = "fichas", "GDU: fichas de parcela o adjudicatario"
        QGIS = "qgis", "GDU: QGIS / edición de capas"
        RELEVAMIENTOS = "relevamientos", "GDU: relevamientos y encuestas"
        LISTADOS = "listados", "GDU: listados y exportaciones"
        OBRAS = "obras", "Obras, certificados y pólizas"
        VIATICOS = "viaticos", "Viáticos y comisiones"
        PERSONAL = "personal", "Personal / RRHH"
        USUARIOS = "usuarios", "Usuarios y permisos"
        OTRO = "otro", "Otro / no sé"

    class Tipo(models.TextChoices):
        PROBLEMA = "problema", "Algo no funciona"
        MEJORA = "mejora", "Mejorar algo que existe"
        NUEVO = "nuevo", "Algo nuevo"

    class Urgencia(models.IntegerChoices):
        # El valor ordena: menor = más urgente.
        BLOQUEA = 1, "Me bloquea el trabajo"
        SEGUIDO = 2, "Me complica seguido"
        MEJOR = 3, "Sería bueno tenerlo"

    class Estado(models.TextChoices):
        NUEVA = "nueva", "Nueva"
        HABLAR = "hablar", "Para hablar en persona"
        CURSO = "curso", "En curso"
        RESUELTA = "resuelta", "Resuelta"
        DESCARTADA = "descartada", "Descartada"

    ESTADOS_CERRADOS = (Estado.RESUELTA, Estado.DESCARTADA)

    titulo = models.CharField("¿Qué necesitás?", max_length=150)
    detalle = models.TextField("Contalo con tus palabras", blank=True)
    ejemplo = models.CharField("Ejemplo concreto", max_length=300, blank=True,
                               help_text="N° de parcela, barrio, expediente, pantalla…")
    modulo = models.CharField("Parte del sistema", max_length=20, choices=Modulo.choices, default=Modulo.OTRO)
    tipo = models.CharField("Tipo", max_length=10, choices=Tipo.choices, default=Tipo.PROBLEMA)
    urgencia = models.PositiveSmallIntegerField("¿Cuánto te afecta?", choices=Urgencia.choices,
                                                default=Urgencia.SEGUIDO)

    # Sin FK a CustomUser: esta tabla puede vivir en otra base (ver routers.py).
    autor_username = models.CharField(max_length=150, db_index=True)
    autor_nombre = models.CharField(max_length=300, blank=True)
    oficina = models.CharField("Tu oficina o área", max_length=120, blank=True)

    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.NUEVA, db_index=True)
    respuesta = models.TextField("Respuesta", blank=True)
    respondido_por = models.CharField(max_length=150, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    editado = models.DateTimeField(null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "necesidad"
        verbose_name_plural = "necesidades"
        ordering = ["urgencia", "-creado"]
        permissions = [
            ("gestionar_necesidad", "Puede cambiar el estado y responder necesidades"),
        ]

    def __str__(self):
        return self.titulo

    @property
    def cerrada(self):
        return self.estado in self.ESTADOS_CERRADOS


class Apoyo(models.Model):
    """'A mí también me pasa': un usuario que se suma a la necesidad de otro."""

    necesidad = models.ForeignKey(Necesidad, on_delete=models.CASCADE, related_name="apoyos")
    username = models.CharField(max_length=150)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["necesidad", "username"], name="apoyo_unico_por_usuario"),
        ]

    def __str__(self):
        return f"{self.username} → {self.necesidad_id}"
