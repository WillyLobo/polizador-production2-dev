---
symbol: select2_programa
kind: function
module: api/views/select2_views.py
lines: 70-86
signature_hash: sha1:4d5ebd781e07fc96dc0cb68c39cbccc22ff0b300
authored: true
---

# select2_programa

**Módulo:** `api/views/select2_views.py` (líneas 70-86)

## Propósito

Endpoint de autocompletar sin paginar (límite fijo de 20 resultados) para un `<select>` select2 configurado a mano — mismo formato `{id, text}` que `carga.views.ajaxviews.get_agentes`, no el mecanismo `django-select2`/`ModelSelect2Widget` que usa el resto del sitio. Busca `carga.Programa` por nombre.

## Firma

```python
def select2_programa(request, q: str=None):
```

## Uso real

`GET /v1/api/select2_programa/?q=`.

## Ver también

- [Programa](../../../carga/models/Programa.md)
