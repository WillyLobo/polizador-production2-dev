---
symbol: _cargotipo_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 470-477
signature_hash: sha1:726a3346526ff72cb871dd669f040613763cef40
authored: true
---
# _cargotipo_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 470-477)

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