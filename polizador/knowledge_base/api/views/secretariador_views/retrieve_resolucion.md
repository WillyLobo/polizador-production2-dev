---
symbol: retrieve_resolucion
kind: function
module: api/views/secretariador_views.py
lines: 105-106
signature_hash: sha1:9359357b280281bde2b1295ca84df8bc25875dec
authored: true
---

# retrieve_resolucion

**Módulo:** `api/views/secretariador_views.py` (líneas 105-106)

## Propósito

Devuelve un `InstrumentosLegalesResoluciones` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_resolucion(request, id: int):
```

## Uso real

`GET /v1/api/resolucione/{{id}}/` — response=`InstrumentosLegalesResolucionesOut`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
