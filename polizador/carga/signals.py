from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import FojaDeMedicion, PlanDeTrabajosEtapa, ContratoMonto, ContratoTramoPago


@receiver(pre_save, sender=FojaDeMedicion)
def auto_increment_foja_numero(sender, instance, **kwargs):
    """Auto-incrementa el número de foja para mantener continuidad.

    Las fojas legacy (`foja_legacy=True`) traen su `foja_numero` ya asignado a mano
    por el form antes de llegar acá, y no deben ser tocadas.
    """
    if instance.foja_legacy:
        return

    if not instance.pk:
        chain_ids = instance.foja_rubro.rubro_cadena_ids()
        last_foja = FojaDeMedicion.objects.filter(
            foja_rubro_id__in=chain_ids
        ).order_by('-foja_numero').first()

        instance.foja_numero = (
            last_foja.foja_numero + 1
            if last_foja
            else instance.foja_rubro.rubro_foja_numero_inicial
        )


@receiver(pre_save, sender=PlanDeTrabajosEtapa)
def auto_increment_etapa_numero(sender, instance, **kwargs):
    """Auto-incrementa el número de etapa para mantener continuidad ante reprogramaciones."""
    if not instance.pk:
        chain_ids = instance.etapa_rubro.rubro_cadena_ids()
        last_etapa = PlanDeTrabajosEtapa.objects.filter(
            etapa_rubro_id__in=chain_ids
        ).order_by('-etapa_numero').first()

        instance.etapa_numero = (last_etapa.etapa_numero + 1) if last_etapa else 1


@receiver(post_save, sender=ContratoMonto)
@receiver(post_delete, sender=ContratoMonto)
def recalcular_montos_obra(sender, instance, **kwargs):
    """Mantiene los montos de Obra sincronizados con los ContratoMonto de sus Contratos."""
    instance.contratomonto_contrato.contrato_obra.recalcular_montos_contrato()


@receiver(pre_save, sender=ContratoTramoPago)
def auto_increment_tramo_numero(sender, instance, **kwargs):
    """Auto-incrementa el número de tramo para mantener continuidad."""
    if not instance.pk:
        last_tramo = ContratoTramoPago.objects.filter(
            tramo_contrato=instance.tramo_contrato
        ).order_by('-tramo_numero').first()

        instance.tramo_numero = (last_tramo.tramo_numero + 1) if last_tramo else 1
