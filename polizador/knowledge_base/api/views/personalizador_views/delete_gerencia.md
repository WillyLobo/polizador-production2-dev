---
symbol: delete_gerencia
kind: function
module: api/views/personalizador_views.py
lines: 68-70
signature_hash: sha1:ce128c243ce365127447405e0adfa8cacb90f6a5
authored: true
---

# delete_gerencia

**Módulo:** `api/views/personalizador_views.py` (líneas 68-70)

## Propósito

Borrado físico (no soft-delete) de un `Gerencia` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_gerencia(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Gerencia](../../../personalizador/models/Gerencia.md)
