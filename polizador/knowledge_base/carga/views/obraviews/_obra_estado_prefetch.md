---
symbol: _obra_estado_prefetch
kind: function
module: carga/views/obraviews.py
lines: 24-60
signature_hash: sha1:07b55b26c9ef4dbc72cc9377069cd3ba8ef6a5ff
authored: false
---

# _obra_estado_prefetch

**Módulo:** `carga/views/obraviews.py` (líneas 24-60)

## Propósito

_(pendiente de autoría)_

## Firma

```python
def _obra_estado_prefetch():
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/views/obraviews.py:124` — `prefetch = _obra_estado_prefetch()`
- `carga/views/obraviews.py:129` — `Prefetch("obra_madre", queryset=Obra.objects.prefetch_related(*_obra_estado_prefetch())),`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
