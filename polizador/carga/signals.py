from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import FojaDeMedicion, ContratoMonto


@receiver(pre_save, sender=FojaDeMedicion)
def auto_increment_foja_numero(sender, instance, **kwargs):
    """Auto-incrementa el número de foja para mantener continuidad."""
    if not instance.pk:
        chain_ids = instance.foja_rubro.rubro_cadena_ids()
        last_foja = FojaDeMedicion.objects.filter(
            foja_rubro_id__in=chain_ids
        ).order_by('-foja_numero').first()

        instance.foja_numero = (last_foja.foja_numero + 1) if last_foja else 1


@receiver(post_save, sender=ContratoMonto)
@receiver(post_delete, sender=ContratoMonto)
def recalcular_montos_obra(sender, instance, **kwargs):
    """Mantiene los montos de Obra sincronizados con los ContratoMonto de sus Contratos."""
    instance.contratomonto_contrato.contrato_obra.recalcular_montos_contrato()
