---
symbol: _obra_ext_datatable_row
kind: function
module: api/views/carga_views.py
lines: 1019-1069
signature_hash: sha1:487d093bf5778ca9095a7159fe8019ea2efe4feb
authored: true
---

# _obra_ext_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 1019-1069)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. La variante "extendida" (~30 columnas — todos los campos de Obra, no solo los de resumen), usada por el listado de exportación. Usa `clip_value_html`/`format_thousands` (`generics.py`) para truncar textos largos y formatear montos con separador de miles.

## Firma

```python
def _obra_ext_datatable_row(o: Obra, user) -> dict:
```

## Uso real

`datatable_obras_extendida` (mismo módulo, más abajo).

## Ver también

- [Obra](../../../carga/models/Obra.md)
- [_obra_datatable_row](_obra_datatable_row.md) — la variante resumida.
