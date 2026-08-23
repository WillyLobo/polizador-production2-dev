---
symbol: _cargotipo_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 480-487
signature_hash: sha1:9af0286494af3b1c1b075e96f4e7a9176a1778a8
authored: true
---

# _cargotipo_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 480-487)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `CargoTipo`: id + tipo.

## Firma

```python
def _cargotipo_datatable_row(c: CargoTipo, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, CargoTipo, ...)` (misma sección del módulo).

## Ver también

- [CargoTipo](../../../personalizador/models/CargoTipo.md)
