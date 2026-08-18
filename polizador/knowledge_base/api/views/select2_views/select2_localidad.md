---
symbol: select2_localidad
kind: function
module: api/views/select2_views.py
lines: 30-46
signature_hash: sha1:a132d116823d82fe135bf452f599410184976b0a
authored: true
---

# select2_localidad

**Módulo:** `api/views/select2_views.py` (líneas 30-46)

## Propósito

Endpoint de autocompletar sin paginar (límite fijo de 20 resultados) para un `<select>` select2 configurado a mano — mismo formato `{id, text}` que `carga.views.ajaxviews.get_agentes`, no el mecanismo `django-select2`/`ModelSelect2Widget` que usa el resto del sitio. Busca `carga.Localidad` por nombre.

## Firma

```python
def select2_localidad(request, q: str=None):
```

## Uso real

`GET /v1/api/select2_localidad/?q=`.

## Ver también

- [Localidad](../../../carga/models/Localidad.md)
