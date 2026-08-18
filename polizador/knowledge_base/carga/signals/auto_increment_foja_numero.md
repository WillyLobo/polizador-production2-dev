---
symbol: auto_increment_foja_numero
kind: function
module: carga/signals.py
lines: 7-26
signature_hash: sha1:3b200e7c07283647e9628921df4f5b044e5ed5c6
authored: true
---

# auto_increment_foja_numero

**Módulo:** `carga/signals.py` (líneas 7-26) · receiver de `pre_save` sobre `FojaDeMedicion`

## Propósito

Asigna `foja_numero` automáticamente cuando se crea una `FojaDeMedicion` nueva, en vez de
dejar que se cargue a mano: busca la última Foja de la misma cadena de rubro
(`rubro_cadena_ids()`, que sigue reprogramaciones vía `rubro_anterior`) y le suma 1. Si es
la primera Foja de la cadena, arranca en `rubro_foja_numero_inicial` (un valor cargado a
mano en el Rubro, para poder continuar la numeración cuando hubo fojas anteriores
registradas fuera del sistema).

Las fojas legacy (`foja_legacy=True`) se saltean por completo: traen su `foja_numero` ya
asignado a mano por el form antes de llegar a esta señal, y no deben ser tocadas — son
justamente el mecanismo para cargar el historial previo sin que la auto-numeración lo
pise.

Por qué es `pre_save` y no una lógica en `save()`: `FojaDeMedicionItem` (ver
[recalcular_acumulado_fojas_siguientes](recalcular_acumulado_fojas_siguientes.md)) necesita
que `foja_numero` ya esté asignado al momento en que sus items se guardan, y separar la
numeración en una señal la mantiene desacoplada del resto de la lógica de `save()` del
modelo (que no tiene override propio).

## Firma

```python
def auto_increment_foja_numero(sender, instance, **kwargs):
```

## Uso real

No se llama directamente. Se dispara al guardar una `FojaDeMedicion` nueva, típicamente
desde `CrearFojaDeMedicion`:

```python
# carga/views/fojademedicionviews.py (CrearFojaDeMedicion.form_valid)
self.object = form.save()  # pre_save -> asigna foja_numero antes del INSERT
```

## Flujo de datos

1. Si `instance.foja_legacy` es `True` → no hace nada, se respeta el número cargado a mano.
2. Si `instance.pk` ya existe (es una edición, no una creación) → tampoco hace nada:
   `foja_numero` se asigna una sola vez, al crear.
3. Si es una Foja nueva: busca `FojaDeMedicion.objects.filter(foja_rubro_id__in=chain_ids).order_by('-foja_numero').first()` dentro de la cadena de rubro, y asigna `last_foja.foja_numero + 1` (o `rubro_foja_numero_inicial` si no hay ninguna todavía).

## Ver también

- [FojaDeMedicion](../models/FojaDeMedicion.md)
- [recalcular_acumulado_fojas_siguientes](recalcular_acumulado_fojas_siguientes.md) — depende de que `foja_numero` ya esté asignado para poder ubicar la Foja "siguiente" en la cadena.
- [auto_increment_etapa_numero](auto_increment_etapa_numero.md) — mismo patrón aplicado a `PlanDeTrabajosEtapa`.
