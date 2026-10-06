---
symbol: _empresa_datatable_row
kind: function
module: api/views/carga_views.py
lines: 262-280
signature_hash: sha1:c99db5b0d77a2960dfa2e6638ac2ecb25ec30e81
authored: true
---

# _empresa_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 262-280)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Empresa`: nombre, CUIT, titular, dirección.

## Firma

```python
def _empresa_datatable_row(e: Empresa, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Empresa, ...)` (misma sección del módulo).

## Ver también

- [Empresa](../../../carga/models/Empresa.md)
