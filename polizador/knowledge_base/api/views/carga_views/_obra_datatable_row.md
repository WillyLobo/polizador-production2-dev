---
symbol: _obra_datatable_row
kind: function
module: api/views/carga_views.py
lines: 838-862
signature_hash: sha1:160f843406dc7510146f12375900a999906da35e
authored: true
---

# _obra_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 838-862)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Lee `obra_acum_pct_anotado`/`obra_anticipo_acumulado_anotado` como atributos anotados por queryset (`getattr(o, ..., None)`, no propiedades del modelo) — asume que quien arma el queryset (`datatable_obras`) ya corrió `carga.obras_con_acumulado_anotado()`.

## Firma

```python
def _obra_datatable_row(o: Obra, user) -> dict:
```

## Uso real

`datatable_obras` (mismo módulo, más abajo).

## Ver también

- [Obra](../../../carga/models/Obra.md)
- [obras_con_acumulado_anotado](../../../carga/models/obras_con_acumulado_anotado.md)
