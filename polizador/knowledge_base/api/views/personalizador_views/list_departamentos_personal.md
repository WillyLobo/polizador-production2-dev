---
symbol: list_departamentos_personal
kind: function
module: api/views/personalizador_views.py
lines: 98-99
signature_hash: sha1:e491af5998572ce70a78ce97da0c47a006122b9b
authored: true
---

# list_departamentos_personal

**Módulo:** `api/views/personalizador_views.py` (líneas 98-99)

## Propósito

Listado paginado (`PerPagePagination`) de `Departamento`, gateado por `require_model_perm(Departamento)` (permiso `view_<modelo>`). Mismo patrón: sin `retrieve`/`update`.

## Firma

```python
def list_departamentos_personal(request):
```

## Uso real

`GET /v1/api/departamentos-personal/` — response=`List[DepartamentoOut]`.

## Ver también

- [Departamento](../../../personalizador/models/Departamento.md)
