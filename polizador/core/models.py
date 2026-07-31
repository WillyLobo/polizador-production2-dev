from django.conf import settings
from django.db import models


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
