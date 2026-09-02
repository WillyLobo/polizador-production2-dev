---
symbol: datatable_solicitudes_filtro_vehiculos
kind: function
module: api/views/secretariador_views.py
lines: 789-796
signature_hash: sha1:4e866884be2b00852383332a96a1a83d8eec6512
authored: true
---
# datatable_solicitudes_filtro_vehiculos

**Módulo:** `api/views/secretariador_views.py` (líneas 789-796)

## Propósito

Choices `(id, vehiculo_str)` de Vehículos efectivamente usados en alguna Solicitud.

## Firma

```python
def datatable_solicitudes_filtro_vehiculos(request):
```

## Uso real

`GET /v1/api/datatables/solicitudes/filtro-vehiculos/`.

## Ver también

- [Vehiculo](../../../secretariador/models/Vehiculo.md)