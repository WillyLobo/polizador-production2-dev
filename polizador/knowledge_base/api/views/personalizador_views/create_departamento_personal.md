---
symbol: create_departamento_personal
kind: function
module: api/views/personalizador_views.py
lines: 104-105
signature_hash: sha1:c6d9ac8a9f2d908ed0494bac2dc03226c263d4b4
authored: true
---

# create_departamento_personal

**Módulo:** `api/views/personalizador_views.py` (líneas 104-105)

## Propósito

Alta de `Departamento` desde `DepartamentoCreate` (`payload.model_dump()` directo a `Departamento.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_departamento_personal(request, payload: DepartamentoPerCreate):
```

## Uso real

`POST /v1/api/departamentos-personal/` — response=`DepartamentoOut`.

## Ver también

- [Departamento](../../../personalizador/models/Departamento.md)
