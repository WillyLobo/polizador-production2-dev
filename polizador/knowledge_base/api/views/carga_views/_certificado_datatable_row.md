---
symbol: _certificado_datatable_row
kind: function
module: api/views/carga_views.py
lines: 1327-1353
signature_hash: sha1:48c5701f56a458dc3358201b3cda8e86d2e190e7
authored: true
---

# _certificado_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 1327-1353)

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
