---
symbol: _vehiculo_datatable_row
kind: function
module: api/views/secretariador_views.py
lines: 534-553
signature_hash: sha1:f31bcf6eaa77ed38ab7213316b193fbc5186b631
authored: true
---

# _vehiculo_datatable_row

**Módulo:** `api/views/secretariador_views.py` (líneas 534-553)

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
