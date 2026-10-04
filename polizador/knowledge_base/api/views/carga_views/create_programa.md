---
symbol: create_programa
kind: function
module: api/views/carga_views.py
lines: 318-319
signature_hash: sha1:1d8fe6fb5f4871f014b2f317adfd9527732794ce
authored: true
---

# create_programa

**Módulo:** `api/views/carga_views.py` (líneas 318-319)

## Propósito

Alta de `Programa` desde `ProgramaCreate` (`payload.model_dump()` directo a `Programa.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_programa(request, payload: ProgramaCreate):
```

## Uso real

`POST /v1/api/programas/` — response=`ProgramaOut`.

## Ver también

- [Programa](../../../carga/models/Programa.md)
