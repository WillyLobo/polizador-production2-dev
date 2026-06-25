from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import FojaDeMedicion


@receiver(pre_save, sender=FojaDeMedicion)
def auto_increment_foja_numero(sender, instance, **kwargs):
    """Auto-incrementa el número de foja para mantener continuidad."""
    if not instance.pk:
        chain_ids = instance.foja_rubro.rubro_cadena_ids()
        last_foja = FojaDeMedicion.objects.filter(
            foja_rubro_id__in=chain_ids
        ).order_by('-foja_numero').first()

        instance.foja_numero = (last_foja.foja_numero + 1) if last_foja else 1
