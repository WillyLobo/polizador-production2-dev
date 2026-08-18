---
symbol: _departamento_carga_datatable_row
kind: function
module: api/views/carga_views.py
lines: 496-507
signature_hash: sha1:3edcc778d454bcfde96821bba80f32fc1fca24c0
authored: true
---

# _departamento_carga_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 496-507)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Departamento`: id + nombre.

## Firma

```python
def _departamento_carga_datatable_row(d: Departamento, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Departamento, ...)` (misma sección del módulo).

## Ver también

- [Departamento](../../../carga/models/Departamento.md)
