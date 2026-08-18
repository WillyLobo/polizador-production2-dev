---
symbol: PerPagePagination
kind: class
module: api/views/generics.py
lines: 16-43
signature_hash: sha1:57e4228e83b1a84088266426b015eca8d94535d0
authored: true
---

# PerPagePagination

**Módulo:** `api/views/generics.py` (líneas 16-43) · hereda de `PaginationBase`

## Propósito

Adapta el mecanismo de paginación de `django-ninja` (`PaginationBase`) al contrato original de esta API (`?page=&per_page=` → `{count, next, previous, results}`) — para que los endpoints `list_*` migrados desde el esquema anterior no rompieran el contrato que ya consumían los datatables JS existentes, en vez de adoptar el estilo `limit/offset` por defecto de ninja.

## Firma

```python
class PerPagePagination(PaginationBase):
```

## Uso real

`@paginate(PerPagePagination)` en prácticamente todos los `list_*` de `carga_views.py`/`personalizador_views.py`/`secretariador_views.py`.

## Ver también

_(sin referencias cruzadas)_
