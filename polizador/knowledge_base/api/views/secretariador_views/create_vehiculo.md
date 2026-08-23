---
symbol: create_vehiculo
kind: function
module: api/views/secretariador_views.py
lines: 523-524
signature_hash: sha1:0c0f399fdc4cf4b93eefe1c10947ff9ecdc9200c
authored: true
---

# create_vehiculo

**Módulo:** `api/views/secretariador_views.py` (líneas 523-524)

## Propósito

Alta de `Vehiculo` desde `VehiculoCreate` (`payload.model_dump()` directo a `Vehiculo.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_vehiculo(request, payload: VehiculoCreate):
```

## Uso real

`POST /v1/api/vehiculos/` — response=`VehiculoOut`.

## Ver también

- [Vehiculo](../../../secretariador/models/Vehiculo.md)
