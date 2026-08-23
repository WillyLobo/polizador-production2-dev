---
symbol: _memorandum_datatable_row
kind: function
module: api/views/secretariador_views.py
lines: 195-215
signature_hash: sha1:7c258510855c6d94dd3f27bdd7868d6c05a30ec9
authored: true
---

# _memorandum_datatable_row

**Módulo:** `api/views/secretariador_views.py` (líneas 195-215)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `InstrumentosLegalesMemorandum`: tipo, número, año, fecha, descripción, texto OCR (truncado con `clip_value_html`).

## Firma

```python
def _memorandum_datatable_row(m: InstrumentosLegalesMemorandum, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, InstrumentosLegalesMemorandum, ...)` (misma sección del módulo).

## Ver también

- [InstrumentosLegalesMemorandum](../../../secretariador/models/InstrumentosLegalesMemorandum.md)
