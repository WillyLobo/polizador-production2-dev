---
symbol: list_users
kind: function
module: api/views/personalizador_views.py
lines: 42-43
signature_hash: sha1:6b29d8cc0c3abe02ee798a4a7193bceccd17d938
authored: true
---

# list_users

**Módulo:** `api/views/personalizador_views.py` (líneas 42-43)

## Propósito

Listado paginado de `CustomUser` (el modelo de autenticación, `AUTH_USER_MODEL` — no confundir con `Agente`).

## Firma

```python
def list_users(request):
```

## Uso real

`GET /v1/api/users/` — response=`List[CustomUserOut]`.

## Ver también

- [CustomUser](../../../personalizador/models/CustomUser.md)
