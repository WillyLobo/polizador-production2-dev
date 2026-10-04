---
symbol: create_conjunto
kind: function
module: api/views/carga_views.py
lines: 1487-1488
signature_hash: sha1:8e7f4d96035f920b4f22542fb50f71237e0c9736
authored: true
---

# create_conjunto

**Módulo:** `api/views/carga_views.py` (líneas 1487-1488)

## Propósito

Alta de `ConjuntoLicitado` desde `ConjuntoLicitadoCreate` (`payload.model_dump()` directo a `ConjuntoLicitado.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_conjunto(request, payload: ConjuntoLicitadoCreate):
```

## Uso real

`POST /v1/api/conjuntos/` — response=`ConjuntoLicitadoOut`.

## Ver también

- [ConjuntoLicitado](../../../carga/models/ConjuntoLicitado.md)
