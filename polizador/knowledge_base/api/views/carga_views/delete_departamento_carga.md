---
symbol: delete_departamento_carga
kind: function
module: api/views/carga_views.py
lines: 491-493
signature_hash: sha1:63f3e9b81c1522274ff25c11946e947d0e38c475
authored: true
---

# delete_departamento_carga

**Módulo:** `api/views/carga_views.py` (líneas 491-493)

## Propósito

Borrado físico (no soft-delete) de un `Departamento` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_departamento_carga(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Departamento](../../../carga/models/Departamento.md)
