---
symbol: list_programas
kind: function
module: api/views/carga_views.py
lines: 306-307
signature_hash: sha1:d58d77e1fe5b7570ff873ea52f63bcc6fd0ae3ae
authored: true
---

# list_programas

**Módulo:** `api/views/carga_views.py` (líneas 306-307)

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
