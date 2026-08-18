---
symbol: _resolucion_directorio_datatable_row
kind: function
module: api/views/secretariador_views.py
lines: 393-414
signature_hash: sha1:df00575201330518b2df065ebc4996519b997943
authored: true
---

# _resolucion_directorio_datatable_row

**Módulo:** `api/views/secretariador_views.py` (líneas 393-414)

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
