---
symbol: _tipolicenciapermiso_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 860-881
signature_hash: sha1:9bfa5a40c1f6f9a7a561c870e34b8a8fd8f887ee
authored: true
---

# _tipolicenciapermiso_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 860-881)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. `tipolicenciapermiso_tope` combina cantidad+período en una sola columna legible ("N (Por año calendario)"), o "Variable" si el tope no es un número fijo (`tipolicenciapermiso_tope_cantidad is None`).

## Firma

```python
def _tipolicenciapermiso_datatable_row(t: TipoLicenciaPermiso, user) -> dict:
```

## Uso real

`register_simple_datatable(router, TipoLicenciaPermiso, "tipolicenciapermisos", ...)`.

## Ver también

- [TipoLicenciaPermiso](../../../personalizador/models/TipoLicenciaPermiso.md)
