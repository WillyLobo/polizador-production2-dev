---
symbol: _oficina_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 647-661
signature_hash: sha1:e409d70aeb507d669b6c66bf384861560135a64a
authored: true
---

# _oficina_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 647-661)

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
