---
symbol: BaseFojaDeMedicionItemFormset
kind: class
module: carga/forms/fojademedicionforms.py
lines: 152-206
signature_hash: sha1:99f8edbbcd813dd24379aeacd6321f8fc54a74e0
authored: true
---

# BaseFojaDeMedicionItemFormset

**Módulo:** `carga/forms/fojademedicionforms.py` (líneas 152-206) · hereda de `BaseInlineFormSet`

## Propósito

Valida los items de una Foja entre sí y contra la Foja anterior del mismo rubro — la
contraparte, a nivel formset (antes de guardar nada), de lo que
[recalcular_acumulado_fojas_siguientes](../../signals/recalcular_acumulado_fojas_siguientes.md)
hace a nivel señal (después de guardar, hacia adelante). `_anterior_map()` resuelve el
acumulado anterior de cada item candidato; `clean()` chequea, por item, que Anterior + Mes
no supere la Incidencia fija del item, y en conjunto, que ninguno de los tres totales
(Anterior/Mes/Acumulado) supere 100% en toda la Foja.

## Firma

```python
class BaseFojaDeMedicionItemFormset(BaseInlineFormSet):
```

## Uso real

`formset=BaseFojaDeMedicionItemFormset` en `FojaDeMedicionItemFormset`/`build_foja_item_formset_class`.

## Ver también

- [FojaDeMedicionItem](../../models/FojaDeMedicionItem.md)
- [recalcular_acumulado_fojas_siguientes](../../signals/recalcular_acumulado_fojas_siguientes.md)
