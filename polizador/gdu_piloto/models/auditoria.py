from django.contrib.gis.db import models

# managed=False: tablas/vistas de la base GDU heredada (migrada desde el proyecto hasura),
# el schema real vive fuera del control de las migraciones de Django.


class AuditLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    tstamp = models.DateTimeField()
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    client_addr = models.GenericIPAddressField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.action} ({self.tstamp})"

    class Meta:
        managed = False
        db_table = '"audit"."audit_logs"'
        db_table_comment = 'tabla de log de actividades de usuarios del visualizador'

