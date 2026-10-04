---
symbol: list_obras
kind: function
module: api/views/carga_views.py
lines: 707-723
signature_hash: sha1:af787d4ad78a3f10a5e2711e06d9c5b737efca46
authored: true
---

# list_obras

**Módulo:** `api/views/carga_views.py` (líneas 707-723)

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
