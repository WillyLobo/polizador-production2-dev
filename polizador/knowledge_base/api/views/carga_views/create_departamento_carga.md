---
symbol: create_departamento_carga
kind: function
module: api/views/carga_views.py
lines: 476-477
signature_hash: sha1:da6540f2a3a4af29e25d1f771e5e510ec88cdf37
authored: true
---

# create_departamento_carga

**Módulo:** `api/views/carga_views.py` (líneas 476-477)

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
