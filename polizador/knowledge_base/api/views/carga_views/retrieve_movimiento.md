---
symbol: retrieve_movimiento
kind: function
module: api/views/carga_views.py
lines: 1920-1921
signature_hash: sha1:a6f687fd8ff93a5b04c7675b95e70dc1334ec92b
authored: true
---

# retrieve_movimiento

**Módulo:** `api/views/carga_views.py` (líneas 1920-1921)

## Propósito

Devuelve un `Poliza_Movimiento` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_movimiento(request, id: int):
```

## Uso real

`GET /v1/api/movimiento/{{id}}/` — response=`Poliza_MovimientoOut`.

## Ver también

- [Poliza_Movimiento](../../../carga/models/Poliza_Movimiento.md)
- [Poliza](../../../carga/models/Poliza.md)
