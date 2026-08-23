---
symbol: datatable_agentes_filtro_denominacion
kind: function
module: api/views/personalizador_views.py
lines: 793-800
signature_hash: sha1:7c1ca319b0e0002821ade12f3e65f2c6f01cc70a
authored: true
---

# datatable_agentes_filtro_denominacion

**Módulo:** `api/views/personalizador_views.py` (líneas 793-800)

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
