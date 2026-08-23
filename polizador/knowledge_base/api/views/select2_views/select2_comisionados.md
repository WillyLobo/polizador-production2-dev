---
symbol: select2_comisionados
kind: function
module: api/views/select2_views.py
lines: 10-26
signature_hash: sha1:1e88b8df6f8db0edb04f94df86eaa34ccad299ca
authored: true
---

# select2_comisionados

**Módulo:** `api/views/select2_views.py` (líneas 10-26)

## Propósito

Endpoint de autocompletar sin paginar (límite fijo de 20 resultados) para un `<select>` select2 configurado a mano — mismo formato `{id, text}` que `carga.views.ajaxviews.get_agentes`, no el mecanismo `django-select2`/`ModelSelect2Widget` que usa el resto del sitio. Busca `personalizador.Agente` por nombre y apellido combinados (`agente_nombreyapellido__icontains`).

## Firma

```python
def select2_comisionados(request, q: str=None):
```

## Uso real

`GET /v1/api/select2_comisionado/?q=`.

## Ver también

- [Agente](../../../personalizador/models/Agente.md)
