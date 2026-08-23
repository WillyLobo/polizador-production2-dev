---
symbol: SchemaDocsView
kind: class
module: core/views.py
lines: 27-28
signature_hash: sha1:5e2c591386531d1b67b807b84538cf0ee66c798a
authored: true
---

# SchemaDocsView

**Módulo:** `core/views.py` (líneas 27-28) · hereda de `SuperuserRequiredMixin, TemplateView`

## Propósito

Sirve el índice del sitio estático generado por SchemaSpy (esquema de la base de datos) — un `TemplateView` sin contexto propio, el sitio foráneo (con su propio bootstrap/AdminLTE, sin extender `base.html`) vive entero bajo `SCHEMA_DOCS_ROOT`. Ver `schema_docs_asset` para cómo se sirven los demás archivos del sitio.

## Firma

```python
class SchemaDocsView(SuperuserRequiredMixin, TemplateView):
```

## Uso real

`SchemaDocsView` (`schema_docs`), enlazada desde el navbar ("Administracion > Externos > Schema de la base de datos").

## Ver también

- [schema_docs_asset](schema_docs_asset.md)
