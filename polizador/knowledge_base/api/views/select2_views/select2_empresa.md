---
symbol: select2_empresa
kind: function
module: api/views/select2_views.py
lines: 50-66
signature_hash: sha1:da3ba64a3bd7e1ea98de144cd2fa4616254e7f6d
authored: true
---

# select2_empresa

**Módulo:** `api/views/select2_views.py` (líneas 50-66)

## Propósito

Endpoint de autocompletar sin paginar (límite fijo de 20 resultados) para un `<select>` select2 configurado a mano — mismo formato `{id, text}` que `carga.views.ajaxviews.get_agentes`, no el mecanismo `django-select2`/`ModelSelect2Widget` que usa el resto del sitio. Busca `carga.Empresa` por nombre.

## Firma

```python
def select2_empresa(request, q: str=None):
```

## Uso real

`GET /v1/api/select2_empresa/?q=`.

## Ver también

- [Empresa](../../../carga/models/Empresa.md)
