---
symbol: auto_increment_etapa_numero
kind: function
module: carga/signals.py
lines: 30-38
signature_hash: sha1:ef5c58ccae0b8185f3e458b4fd7bcae69f0c4be6
authored: true
---

# auto_increment_etapa_numero

**Módulo:** `carga/signals.py` (líneas 30-38) · receiver de `pre_save` sobre `PlanDeTrabajosEtapa`

## Propósito

Mismo patrón que [auto_increment_foja_numero](auto_increment_foja_numero.md) pero para
`PlanDeTrabajosEtapa`: al crear una Etapa nueva, busca la última `etapa_numero` dentro de
la cadena de rubro (`rubro_cadena_ids()`, que sigue `rubro_anterior` a través de
reprogramaciones) y le suma 1. A diferencia de las Fojas, acá no hay concepto de "legacy"
ni de número inicial cargado a mano — siempre arranca en 1 si la cadena todavía no tiene
ninguna Etapa.

Que la numeración siga la cadena de rubro (no solo el rubro puntual) es lo que le permite
sobrevivir a una reprogramación: cuando un Plan de Trabajos se reprograma, el Rubro nuevo
queda enlazado al viejo vía `rubro_anterior`, y las Etapas del nuevo Rubro continúan la
numeración del que reemplazó en vez de arrancar de nuevo desde 1.

## Firma

```python
def auto_increment_etapa_numero(sender, instance, **kwargs):
```

## Uso real

Se dispara al crear cada Etapa desde la vista de carga en grilla (una Etapa por columna,
un item por fila):

```python
# carga/views/plandetrabajosetapaviews.py:102 (PlanDeTrabajosEtapaMatriz.post)
etapa = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)  # pre_save -> asigna etapa_numero
```

## Flujo de datos

1. Si `instance.pk` ya existe (edición) → no hace nada.
2. Si es una Etapa nueva: `PlanDeTrabajosEtapa.objects.filter(etapa_rubro_id__in=chain_ids).order_by('-etapa_numero').first()` dentro de la cadena de rubro, y asigna `last_etapa.etapa_numero + 1` (o `1` si es la primera).

## Ver también

- [PlanDeTrabajosEtapa](../models/PlanDeTrabajosEtapa.md)
- [auto_increment_foja_numero](auto_increment_foja_numero.md) — mismo patrón, aplicado a `FojaDeMedicion`.
