---
symbol: create_empresa
kind: function
module: api/views/carga_views.py
lines: 240-241
signature_hash: sha1:049f3e3917a9b14bbe9543cb4ed3349facff0987
authored: true
---

# create_empresa

**Módulo:** `api/views/carga_views.py` (líneas 240-241)

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
