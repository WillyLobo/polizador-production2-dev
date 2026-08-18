---
symbol: list_programas
kind: function
module: api/views/carga_views.py
lines: 305-306
signature_hash: sha1:a5ffab111729ba7d37ce76549bf857469071db15
authored: true
---

# list_programas

**Módulo:** `api/views/carga_views.py` (líneas 305-306)

## Propósito

Listado paginado (`PerPagePagination`) de `Programa`, gateado por `require_model_perm(Programa)` (permiso `view_<modelo>`).

## Firma

```python
def list_programas(request):
```

## Uso real

`GET /v1/api/programas/` — response=`List[ProgramaOut]`.

## Ver también

- [Programa](../../../carga/models/Programa.md)
