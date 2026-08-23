---
symbol: datatable_obras_extendida_filtro_programa
kind: function
module: api/views/carga_views.py
lines: 1125-1132
signature_hash: sha1:41e9501f110959e48fa5b35b74d4be900b0eee73
authored: true
---

# datatable_obras_extendida_filtro_programa

**Módulo:** `api/views/carga_views.py` (líneas 1125-1132)

## Propósito

Choices `(id, nombre)` de los Programas efectivamente usados por alguna Obra, para el `<select>` de filtro del listado extendido.

## Firma

```python
def datatable_obras_extendida_filtro_programa(request):
```

## Uso real

`GET /v1/api/datatables/obras-extendida/filtro-programa/`.

## Ver también

- [Programa](../../../carga/models/Programa.md)
