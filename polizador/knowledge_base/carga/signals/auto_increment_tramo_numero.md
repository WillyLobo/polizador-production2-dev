---
symbol: auto_increment_tramo_numero
kind: function
module: carga/signals.py
lines: 68-75
signature_hash: sha1:648b0515628bbd7b73c107cbdb5ba1668e95c773
authored: true
---

# auto_increment_tramo_numero

**Módulo:** `carga/signals.py` (líneas 68-75) · receiver de `pre_save` sobre `ContratoTramoPago`

## Propósito

Mismo patrón de auto-numeración que
[auto_increment_foja_numero](auto_increment_foja_numero.md) y
[auto_increment_etapa_numero](auto_increment_etapa_numero.md), acá para
`ContratoTramoPago` (los tramos de pago de un Contrato con certificación por etapas — ver
`Contrato.contrato_certificacion_por_etapas`). Es el más simple de los tres: no hay
concepto de cadena/reprogramación, `tramo_numero` es simplemente correlativo dentro del
mismo `Contrato` (`tramo_contrato`), arrancando en 1.

## Firma

```python
def auto_increment_tramo_numero(sender, instance, **kwargs):
```

## Uso real

Se dispara al guardar el formset de tramos de un Contrato:

```python
# carga/views/contratotramopagoviews.py:35 (GestionarTramosContrato.post)
with transaction.atomic():
    formset.save()  # cada ContratoTramoPago nuevo -> pre_save -> asigna tramo_numero
```

## Flujo de datos

1. Si `instance.pk` ya existe (edición) → no hace nada.
2. Si es un Tramo nuevo: `ContratoTramoPago.objects.filter(tramo_contrato=instance.tramo_contrato).order_by('-tramo_numero').first()`, y asigna `last_tramo.tramo_numero + 1` (o `1` si es el primero del Contrato).

## Ver también

- [ContratoTramoPago](../models/ContratoTramoPago.md)
- [auto_increment_foja_numero](auto_increment_foja_numero.md) / [auto_increment_etapa_numero](auto_increment_etapa_numero.md) — mismo patrón de auto-numeración, con la variante de cadena de rubro.
