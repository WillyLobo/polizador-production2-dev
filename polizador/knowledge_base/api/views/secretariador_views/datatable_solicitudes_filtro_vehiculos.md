---
symbol: datatable_solicitudes_filtro_vehiculos
kind: function
module: api/views/secretariador_views.py
lines: 782-789
signature_hash: sha1:52dffa2be0551991b45cb1bfafe966441e0bee10
authored: true
---

# datatable_solicitudes_filtro_vehiculos

**Módulo:** `api/views/secretariador_views.py` (líneas 782-789)

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
