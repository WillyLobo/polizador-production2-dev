---
symbol: datatable_obras_extendida
kind: function
module: api/views/carga_views.py
lines: 1074-1121
signature_hash: sha1:f7e0b6ea21bdb17552cf919e0f48f757b7c4bb18
authored: true
---

# datatable_obras_extendida

**Módulo:** `api/views/carga_views.py` (líneas 1074-1121)

## Propósito

Mismo patrón que `datatable_obras` pero para el listado extendido (~30 columnas, más `prefetch_related` de M2M). Los filtros que apuntan a un M2M (`obra_departamento_m`/`obra_municipio_m`/`obra_localidad_m`/`obra_principal`) fuerzan `.distinct()` para no duplicar filas por cada match del M2M.

## Firma

```python
def datatable_obras_extendida(request, draw: int=1, start: int=0, length: int=50, search: str='', order_by: str='-id', filters: str='{}'):
```

## Uso real

`GET /v1/api/datatables/obras-extendida/` — consumido por `Lista-obras-extendida.html` (`carga:lista-obras-extendida`).

## Ver también

- [Obra](../../../carga/models/Obra.md)
- [_obra_ext_datatable_row](_obra_ext_datatable_row.md)
