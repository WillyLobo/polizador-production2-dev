---
symbol: _resolucion_directorio_datatable_row
kind: function
module: api/views/secretariador_views.py
lines: 400-421
signature_hash: sha1:7fbee839d7ae660c884a970c66f574049fe0aa19
authored: true
---
# _resolucion_directorio_datatable_row

**Módulo:** `api/views/secretariador_views.py` (líneas 400-421)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Variante solo-Directorio, con columna `instrumentolegalresoluciones_acta` (que la variante combinada no muestra).

## Firma

```python
def _resolucion_directorio_datatable_row(r: InstrumentosLegalesResoluciones, user) -> dict:
```

## Uso real

`register_simple_datatable(router, InstrumentosLegalesResoluciones, "resoluciones-directorio", ..., queryset=...filter(tipo='D'))`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
- [_resolucion_datatable_row](_resolucion_datatable_row.md)