---
symbol: create_decreto
kind: function
module: api/views/secretariador_views.py
lines: 181-184
signature_hash: sha1:d746c5833ad5e4e7cbc29fd7753da02f339d9194
authored: true
---

# create_decreto

**Módulo:** `api/views/secretariador_views.py` (líneas 181-184)

## Propósito

Alta de `InstrumentosLegalesDecretos` desde `InstrumentosLegalesDecretosCreate` (`payload.model_dump()` directo a `InstrumentosLegalesDecretos.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic). Llama `.refresh_from_db()` después del `create()` — necesario para que los `GeneratedField` calculados por la base (ej. `instrumentolegalresoluciones_str`) vengan poblados en la respuesta, ya que `Model.objects.create()` no los recarga solo.

## Firma

```python
def create_decreto(request, payload: DecretoCreate):
```

## Uso real

`POST /v1/api/decretos/` — response=`InstrumentosLegalesDecretosOut`.

## Ver también

- [InstrumentosLegalesDecretos](../../../secretariador/models/InstrumentosLegalesDecretos.md)
