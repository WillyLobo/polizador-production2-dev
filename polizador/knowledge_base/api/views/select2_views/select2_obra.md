---
symbol: select2_obra
kind: function
module: api/views/select2_views.py
lines: 90-106
signature_hash: sha1:f799027274e4e5673f0e13fad55dd6f19ae7b97f
authored: true
---

# select2_obra

**Módulo:** `api/views/select2_views.py` (líneas 90-106)

## Propósito

Endpoint de autocompletar sin paginar (límite fijo de 20 resultados) para un `<select>` select2 configurado a mano — mismo formato `{id, text}` que `carga.views.ajaxviews.get_agentes`, no el mecanismo `django-select2`/`ModelSelect2Widget` que usa el resto del sitio. Busca `carga.Obra` por nombre.

## Firma

```python
def select2_obra(request, q: str=None):
```

## Uso real

`GET /v1/api/select2_obra/?q=`.

## Ver también

- [Obra](../../../carga/models/Obra.md)
