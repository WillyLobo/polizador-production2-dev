---
symbol: _licenciapermiso_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 794-812
signature_hash: sha1:fff66cd33372bf024ad5fbf0d0aff62a12fd7b6d
authored: true
---
# _licenciapermiso_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 794-812)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Distingue "ver" (siempre visible) de "editar"/"eliminar" (según permiso) — a diferencia del patrón `_simple_acciones` de tres ramas, acá el link de detalle no depende de ningún permiso especial.

## Firma

```python
def _licenciapermiso_datatable_row(s: LicenciaPermiso, user) -> dict:
```

## Uso real

`register_simple_datatable(router, LicenciaPermiso, "licenciapermisos", ...)`.

## Ver también

- [LicenciaPermiso](../../../personalizador/models/LicenciaPermiso.md)