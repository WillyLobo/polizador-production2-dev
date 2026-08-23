---
symbol: list_obras
kind: function
module: api/views/carga_views.py
lines: 706-722
signature_hash: sha1:592d69de3c92df6d00014f31ac5e3a17a75237a9
authored: true
---

# list_obras

**Módulo:** `api/views/carga_views.py` (líneas 706-722)

## Propósito

Listado paginado de Obra con filtros por empresa/programa/región (`?empresa=&programa=&region=`) y búsqueda libre `?q=` sobre nombre/expediente/resolución. `select_related` de empresa/programa para evitar N+1 en la serialización.

## Firma

```python
def list_obras(request, empresa: str='', programa: str='', region: str='', q: str=''):
```

## Uso real

`GET /v1/api/obras/` — response=`List[ObraOut]`.

## Ver también

- [Obra](../../../carga/models/Obra.md)
