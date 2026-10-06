---
symbol: _certificado_datatable_row
kind: function
module: api/views/carga_views.py
lines: 1328-1354
signature_hash: sha1:bf17695b36b57f2bdfa775b628fedc9cecb34d6e
authored: true
---

# _certificado_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 1328-1354)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Usa `format_thousands` (`generics.py`) para los montos a cobrar.

## Firma

```python
def _certificado_datatable_row(c: Certificado, user) -> dict:
```

## Uso real

`datatable_certificados` (mismo módulo, más abajo).

## Ver también

- [Certificado](../../../carga/models/Certificado.md)
