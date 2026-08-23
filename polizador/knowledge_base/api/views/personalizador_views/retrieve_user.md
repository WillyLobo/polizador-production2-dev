---
symbol: retrieve_user
kind: function
module: api/views/personalizador_views.py
lines: 48-49
signature_hash: sha1:56c3a489a0d345e01762788b8511dda10ff18ff2
authored: true
---

# retrieve_user

**Módulo:** `api/views/personalizador_views.py` (líneas 48-49)

## Propósito

Devuelve un `CustomUser` puntual por `id`.

## Firma

```python
def retrieve_user(request, id: int):
```

## Uso real

`GET /v1/api/user/{id}/` — response=`CustomUserOut`. Sin endpoints create/update/delete — la gestión de cuentas de usuario no pasa por esta API (allauth/admin de Django).

## Ver también

- [CustomUser](../../../personalizador/models/CustomUser.md)
