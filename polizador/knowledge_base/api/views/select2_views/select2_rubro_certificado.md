---
symbol: select2_rubro_certificado
kind: function
module: api/views/select2_views.py
lines: 130-146
signature_hash: sha1:fde85a18c218b51b1e9b73846e03976e26b522e4
authored: true
---

# select2_rubro_certificado

**Módulo:** `api/views/select2_views.py` (líneas 130-146)

## Propósito

Endpoint de autocompletar sin paginar (límite fijo de 20 resultados) para un `<select>` select2 configurado a mano — mismo formato `{id, text}` que `carga.views.ajaxviews.get_agentes`, no el mecanismo `django-select2`/`ModelSelect2Widget` que usa el resto del sitio. Busca `carga.CertificadoRubro` por nombre.

## Firma

```python
def select2_rubro_certificado(request, q: str=None):
```

## Uso real

`GET /v1/api/select2_rubro_certificado/?q=`.

## Ver también

- [CertificadoRubro](../../../carga/models/CertificadoRubro.md)
