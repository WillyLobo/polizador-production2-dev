---
symbol: _comisionadoexterno_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 227-245
signature_hash: sha1:b3735a5678e29141846d37890d5967d4d874b6c7
authored: true
---

# _comisionadoexterno_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 227-245)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `ComisionadoExterno`: apellidos, nombres, institución de origen, CUIT.

## Firma

```python
def _comisionadoexterno_datatable_row(c: ComisionadoExterno, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, ComisionadoExterno, ...)` (misma sección del módulo).

## Ver también

- [ComisionadoExterno](../../../personalizador/models/ComisionadoExterno.md)
