---
symbol: _certificado_sin_digital_datatable_row
kind: function
module: api/views/carga_views.py
lines: 1424-1437
signature_hash: sha1:e51f6848c978214fa05b2eba4bc778fa9c6cf8ff
authored: true
---

# _certificado_sin_digital_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 1424-1437)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Variante para el listado "certificados sin digital" (Certificados con avance real pero sin PDF adjunto todavía) — solo columna editar, sin detalle ni eliminar; usada vía `register_simple_datatable(..., with_detail=False)`.

## Firma

```python
def _certificado_sin_digital_datatable_row(c: Certificado, user) -> dict:
```

## Uso real

`row_builder` del datatable `certificados-sin-digital` (`register_simple_datatable`, mismo módulo).

## Ver también

- [Certificado](../../../carga/models/Certificado.md)
