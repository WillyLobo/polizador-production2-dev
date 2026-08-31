---
symbol: datatable_agentes_filtro_denominacion
kind: function
module: api/views/personalizador_views.py
lines: 783-790
signature_hash: sha1:1db53bdafdaf16ec09de66dd80b4aea4e092fb3d
authored: true
---
# datatable_agentes_filtro_denominacion

**Módulo:** `api/views/personalizador_views.py` (líneas 783-790)

## Propósito

Choices `(id, denominación)` de `DenominacionCargo` efectivamente usadas por algún Agente, para el `<select>` de filtro del listado de RRHH.

## Firma

```python
def datatable_agentes_filtro_denominacion(request):
```

## Uso real

`GET /v1/api/datatables/agentes/filtro-denominacion/`.

## Ver también

- [DenominacionCargo](../../../personalizador/models/DenominacionCargo.md)