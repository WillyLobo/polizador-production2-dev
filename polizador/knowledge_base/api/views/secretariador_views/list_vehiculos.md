---
symbol: list_vehiculos
kind: function
module: api/views/secretariador_views.py
lines: 515-518
signature_hash: sha1:115c7e84e93a7ed382e7d712ad5fdc561983f7b4
authored: true
---

# list_vehiculos

**Módulo:** `api/views/secretariador_views.py` (líneas 515-518)

## Propósito

Listado paginado (`PerPagePagination`) de `Vehiculo`, gateado por `require_model_perm(Vehiculo)` (permiso `view_<modelo>`). Sin `retrieve`/`update`.

## Firma

```python
def list_vehiculos(request):
```

## Uso real

`GET /v1/api/vehiculos/` — response=`List[VehiculoOut]`.

## Ver también

- [Vehiculo](../../../secretariador/models/Vehiculo.md)
