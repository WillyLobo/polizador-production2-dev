---
symbol: schema_docs_asset
kind: function
module: core/views.py
lines: 54-57
signature_hash: sha1:e9ae8cc30ca747c5926253c2903c82f3dfbbf7a3
authored: true
---

# schema_docs_asset

**Módulo:** `core/views.py` (líneas 54-57)

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
