---
symbol: list_vehiculos
kind: function
module: api/views/secretariador_views.py
lines: 522-525
signature_hash: sha1:9742282197e5fe19f7c952c2e118c22bc9681d8c
authored: true
---
# list_vehiculos

**Módulo:** `api/views/secretariador_views.py` (líneas 522-525)

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