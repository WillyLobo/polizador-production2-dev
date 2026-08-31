---
symbol: _oficina_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 637-651
signature_hash: sha1:0031c330bcdaeca36691db2c198590d935b6de99
authored: true
---
# _oficina_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 637-651)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Columnas de `Oficina`: los cuatro niveles del árbol organizacional (Directorio/Gerencia/Dirección/Departamento).

## Firma

```python
def _oficina_datatable_row(o: Oficina, user) -> dict:
```

## Uso real

`row_builder` pasado a `register_simple_datatable(router, Oficina, ...)` (misma sección del módulo).

## Ver también

- [Oficina](../../../personalizador/models/Oficina.md)