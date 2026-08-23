---
symbol: delete_comisionado
kind: function
module: api/views/secretariador_views.py
lines: 485-487
signature_hash: sha1:a4ec16f1048d6e254c39b572f6bcfb91f671f7b6
authored: true
---

# delete_comisionado

**Módulo:** `api/views/secretariador_views.py` (líneas 485-487)

## Propósito

Borrado físico (no soft-delete) de un `Agente` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_comisionado(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Agente](../../../secretariador/models/Agente.md)
