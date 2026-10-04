---
symbol: create_aseguradora
kind: function
module: api/views/carga_views.py
lines: 173-174
signature_hash: sha1:884562166908c106ecc5ba213fddef78b25e3e9f
authored: true
---

# create_aseguradora

**Módulo:** `api/views/carga_views.py` (líneas 173-174)

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
