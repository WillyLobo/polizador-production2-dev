---
symbol: _vehiculo_datatable_row
kind: function
module: api/views/secretariador_views.py
lines: 541-560
signature_hash: sha1:2d2bcec47db66f65acdd3e70d58b2377f610cd76
authored: true
---
# _vehiculo_datatable_row

**Módulo:** `api/views/secretariador_views.py` (líneas 541-560)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Vehiculo`: carácter, modelo, patente, póliza, aseguradora.

## Firma

```python
def _vehiculo_datatable_row(v: Vehiculo, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Vehiculo, ...)` (misma sección del módulo).

## Ver también

- [Vehiculo](../../../secretariador/models/Vehiculo.md)