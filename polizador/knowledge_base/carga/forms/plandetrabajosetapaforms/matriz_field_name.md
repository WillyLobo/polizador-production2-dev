---
symbol: matriz_field_name
kind: function
module: carga/forms/plandetrabajosetapaforms.py
lines: 5-6
signature_hash: sha1:7e9658a01c2bf77939071f1ad4e282761f3f20fd
authored: false
---

# matriz_field_name

**Módulo:** `carga/forms/plandetrabajosetapaforms.py` (líneas 5-6)

## Propósito

_(pendiente de autoría)_

## Firma

```python
def matriz_field_name(item_pk, col_index):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/views/plandetrabajosetapaviews.py:13` — `from carga.forms.plandetrabajosetapaforms import build_matriz_form, matriz_field_name`
- `carga/views/plandetrabajosetapaviews.py:55` — `"cells": [form[matriz_field_name(item.pk, col)] for col in range(total_columns)],`
- `carga/views/plandetrabajosetapaviews.py:79` — `initial[matriz_field_name(etapaitem.etapaitem_planitem_id, col)] = etapaitem.etapaitem_pct_proyectado_mes`
- `carga/forms/plandetrabajosetapaforms.py:20` — `self.fields[matriz_field_name(item.pk, col)] = forms.DecimalField(`
- `carga/forms/plandetrabajosetapaforms.py:34` — `return self.cleaned_data.get(matriz_field_name(item_pk, col_index)) or Decimal("0")`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
