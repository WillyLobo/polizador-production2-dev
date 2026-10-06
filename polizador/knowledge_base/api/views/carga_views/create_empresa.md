---
symbol: create_empresa
kind: function
module: api/views/carga_views.py
lines: 241-242
signature_hash: sha1:c311adfaa1a2faa0f8267048700e4d39415582a6
authored: true
---

# create_empresa

**Módulo:** `api/views/carga_views.py` (líneas 241-242)

## Propósito

Alta de `Empresa` desde `EmpresaCreate` (`payload.model_dump()` directo a `Empresa.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_empresa(request, payload: EmpresaCreate):
```

## Uso real

`POST /v1/api/empresas/` — response=`EmpresaOut`.

## Ver también

- [Empresa](../../../carga/models/Empresa.md)
