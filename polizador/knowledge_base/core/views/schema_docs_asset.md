---
symbol: schema_docs_asset
kind: function
module: core/views.py
lines: 58-61
signature_hash: sha1:72474c67b063d2d9dac3ebd7ea6bb79b6ce446cd
authored: true
---
# schema_docs_asset

**Módulo:** `core/views.py` (líneas 58-61)

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