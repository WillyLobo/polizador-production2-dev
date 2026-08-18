---
symbol: create_conjunto
kind: function
module: api/views/carga_views.py
lines: 1486-1487
signature_hash: sha1:72f70cf7d0b8415596c7b1725d0a80c4e7a8afeb
authored: true
---

# create_conjunto

**Módulo:** `api/views/carga_views.py` (líneas 1486-1487)

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
