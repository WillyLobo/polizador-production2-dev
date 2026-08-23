---
symbol: create_departamento_carga
kind: function
module: api/views/carga_views.py
lines: 475-476
signature_hash: sha1:2bd01c0f52789adab07b79ddf2a37264c8adce58
authored: true
---

# create_departamento_carga

**Módulo:** `api/views/carga_views.py` (líneas 475-476)

## Propósito

Alta de `Departamento` desde `DepartamentoCreate` (`payload.model_dump()` directo a `Departamento.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_departamento_carga(request, payload: DepartamentoCargaCreate):
```

## Uso real

`POST /v1/api/departamentos-carga/` — response=`DepartamentoOut`.

## Ver también

- [Departamento](../../../carga/models/Departamento.md)
