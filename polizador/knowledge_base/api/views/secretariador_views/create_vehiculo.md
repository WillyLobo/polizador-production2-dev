---
symbol: create_vehiculo
kind: function
module: api/views/secretariador_views.py
lines: 530-531
signature_hash: sha1:ae5b6fc4339d71d94a198de20440f230dbe229b6
authored: true
---
# create_vehiculo

**Módulo:** `api/views/secretariador_views.py` (líneas 530-531)

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