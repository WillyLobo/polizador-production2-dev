---
symbol: datatable_obras_extendida_filtro_programa
kind: function
module: api/views/carga_views.py
lines: 1126-1133
signature_hash: sha1:e3bbc48b04dd8f34b2b49a11204bc3aecbdc9e9a
authored: true
---

# datatable_obras_extendida_filtro_programa

**Módulo:** `api/views/carga_views.py` (líneas 1126-1133)

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
