---
symbol: schema_docs_asset
kind: function
module: core/views.py
lines: 81-84
signature_hash: sha1:9edbd66d3bf656e7548ca7ba3388f577e674c1fe
authored: true
---
# schema_docs_asset

**Módulo:** `core/views.py` (líneas 81-84)

## Propósito

Sirve cada archivo estático del sitio SchemaSpy (CSS/JS/imágenes/HTML de detalle de tabla) bajo `SCHEMA_DOCS_ROOT`, gateado a mano (`if not request.user.is_authenticated or not request.user.is_superuser: raise PermissionDenied` — no puede usar `SuperuserRequiredMixin` porque es una función, no una clase) y delegando en `django.views.static.serve` de Django, que ya es seguro contra path traversal.

## Firma

```python
def schema_docs_asset(request, path):
```

## Uso real

`schema_docs_asset` (`schema_docs_asset`), consumida por los links internos del propio sitio SchemaSpy servido por `SchemaDocsView`.

## Ver también

- [SchemaDocsView](SchemaDocsView.md)