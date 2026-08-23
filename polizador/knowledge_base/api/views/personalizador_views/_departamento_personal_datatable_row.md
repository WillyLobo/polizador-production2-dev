---
symbol: _departamento_personal_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 610-623
signature_hash: sha1:78792e0a61492fef5debc149b03e91dab0fb7ca9
authored: true
---

# _departamento_personal_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 610-623)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Departamento`: nombre, Dirección, CUOF.

## Firma

```python
def _departamento_personal_datatable_row(d: Departamento, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Departamento, ...)` (misma sección del módulo).

## Ver también

- [Departamento](../../../personalizador/models/Departamento.md)
