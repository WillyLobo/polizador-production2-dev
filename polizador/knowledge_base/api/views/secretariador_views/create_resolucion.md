---
symbol: create_resolucion
kind: function
module: api/views/secretariador_views.py
lines: 111-114
signature_hash: sha1:255bc9c33f6b620c4477e01041fb3ea5b2108113
authored: true
---

# create_resolucion

**Módulo:** `api/views/secretariador_views.py` (líneas 111-114)

## Propósito

Alta de `InstrumentosLegalesResoluciones` desde `InstrumentosLegalesResolucionesCreate` (`payload.model_dump()` directo a `InstrumentosLegalesResoluciones.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic). Llama `.refresh_from_db()` después del `create()` — necesario para que los `GeneratedField` calculados por la base (ej. `instrumentolegalresoluciones_str`) vengan poblados en la respuesta, ya que `Model.objects.create()` no los recarga solo.

## Firma

```python
def create_resolucion(request, payload: ResolucionCreate):
```

## Uso real

`POST /v1/api/resoluciones/` — response=`InstrumentosLegalesResolucionesOut`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
