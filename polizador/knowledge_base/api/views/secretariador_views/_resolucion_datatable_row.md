---
symbol: _resolucion_datatable_row
kind: function
module: api/views/secretariador_views.py
lines: 323-351
signature_hash: sha1:6b882977a6b3e440728de0165f788bbc3a28507e
authored: true
---
# _resolucion_datatable_row

**Módulo:** `api/views/secretariador_views.py` (líneas 323-351)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Listado combinado Presidencia+Directorio: el link de editar bifurca según `instrumentolegalresoluciones_tipo` (URL distinta para cada uno, aunque sea el mismo modelo).

## Firma

```python
def _resolucion_datatable_row(r: InstrumentosLegalesResoluciones, user) -> dict:
```

## Uso real

`register_simple_datatable(router, InstrumentosLegalesResoluciones, "resoluciones", ...)`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
- [_resolucion_numero_completo](_resolucion_numero_completo.md)