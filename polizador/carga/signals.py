from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Certificado, FojaDeMedicion, FojaDeMedicionItem, PlanDeTrabajosEtapa, ContratoMonto, ContratoTramoPago


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


@receiver(post_save, sender=FojaDeMedicionItem)
def recalcular_acumulado_fojas_siguientes(sender, instance, **kwargs):
    """FojaDeMedicionItem.save() calcula fojaitem_pct_acumulado como una copia
    (anterior + avance_mes) al momento de guardarse, no como un valor derivado. Si
    después se edita una Foja anterior, las Fojas posteriores quedan con un
    acumulado desactualizado (puede terminar siendo menor al de la Foja que
    corrigieron). Acá se propaga el recálculo en cascada hacia adelante."""
    foja_siguiente = instance.fojaitem_foja.foja_siguiente()
    if not foja_siguiente:
        return

    item_chain_ids = instance.fojaitem_planitem.item_cadena_siguiente_ids()
    item_siguiente = FojaDeMedicionItem.objects.filter(
        fojaitem_foja=foja_siguiente, fojaitem_planitem_id__in=item_chain_ids
    ).first()
    if item_siguiente:
        item_siguiente.save()


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


# Campos del Certificado que el texto de la resolución describe: si cambia
# alguno, el snapshot guardado queda desactualizado.
CAMPOS_TEXTO_RESOLUCION = (
    "certificado_obra_id",
    "certificado_tipo",
    "certificado_financiamiento",
    "certificado_rubro_db_id",
    "certificado_expediente",
    "certificado_periodo",
    "certificado_fecha",
    "certificado_monto_pesos",
    "certificado_monto_uvi",
    "certificado_devolucion_monto",
    "certificado_devolucion_monto_uvi",
    "certificado_devolucion_expte",
    "certificado_fondoreparo_pct",
    "certificado_mes_pct",
    "certificado_ante_pct",
    "certificado_acum_pct",
    "certificado_anticipo_pct",
    "certificado_etapa_pct",
)


@receiver(pre_save, sender=Certificado)
def invalidar_texto_resolucion_por_cambio_de_datos(sender, instance, **kwargs):
    """`certificado_texto_resolucion` es un snapshot del texto de la resolución ya
    resuelto y retocado a mano. Si después cambian los datos que ese texto describe,
    el snapshot queda mintiendo y la pantalla de revisión lo seguiría mostrando tal
    cual. Lo anulamos acá para forzar que se vuelva a resolver desde la plantilla.

    Se usa `.update()` y no `instance.save()` / mutar `instance`:

    - mutar `instance` no alcanza porque Django arma `update_fields` antes de
      emitir esta señal, así que el cambio no se escribiría;
    - un `save()` acá adentro reentraría en la señal y, sobre todo, escribiría una
      segunda fila en `certificado_history` por cada edición.

    `.update()` no toca los GeneratedField con db_persist, que la base recalcula sola.
    """
    if not instance.pk:
        return
    anterior = Certificado.objects.filter(pk=instance.pk).values(
        "certificado_texto_resolucion", *CAMPOS_TEXTO_RESOLUCION
    ).first()
    if anterior is None or anterior["certificado_texto_resolucion"] is None:
        return
    if any(anterior[campo] != getattr(instance, campo) for campo in CAMPOS_TEXTO_RESOLUCION):
        Certificado.objects.filter(pk=instance.pk).update(certificado_texto_resolucion=None)
        instance.certificado_texto_resolucion = None
