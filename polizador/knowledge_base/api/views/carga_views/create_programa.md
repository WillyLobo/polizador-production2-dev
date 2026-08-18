---
symbol: create_programa
kind: function
module: api/views/carga_views.py
lines: 317-318
signature_hash: sha1:424e5d98be1787fdf007b7f998acc17dd07a6bc6
authored: true
---

# create_programa

**Módulo:** `api/views/carga_views.py` (líneas 317-318)

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
