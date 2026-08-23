---
symbol: create_aseguradora
kind: function
module: api/views/carga_views.py
lines: 172-173
signature_hash: sha1:0f5ae82847750a2627ce5e0e5152c0f884eddd66
authored: true
---

# create_aseguradora

**Módulo:** `api/views/carga_views.py` (líneas 172-173)

## Propósito

Alta de `Aseguradora` desde `AseguradoraCreate` (`payload.model_dump()` directo a `Aseguradora.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_aseguradora(request, payload: AseguradoraCreate):
```

## Uso real

`POST /v1/api/aseguradoras/` — response=`AseguradoraOut`.

## Ver también

- [Aseguradora](../../../carga/models/Aseguradora.md)
