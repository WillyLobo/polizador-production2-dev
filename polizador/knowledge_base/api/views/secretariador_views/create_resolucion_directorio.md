---
symbol: create_resolucion_directorio
kind: function
module: api/views/secretariador_views.py
lines: 147-152
signature_hash: sha1:ca46afb7ffa5b62ca6a2dac9908165b211f0b03f
authored: true
---

# create_resolucion_directorio

**Módulo:** `api/views/secretariador_views.py` (líneas 147-152)

## Propósito

Alta de `InstrumentosLegalesResoluciones` desde `InstrumentosLegalesResolucionesCreate` (`payload.model_dump()` directo a `InstrumentosLegalesResoluciones.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic). Fuerza `instrumentolegalresoluciones_tipo='D'` en el payload antes de crear, sin importar lo que traiga el schema. Llama `.refresh_from_db()` después del `create()` — necesario para que los `GeneratedField` calculados por la base (ej. `instrumentolegalresoluciones_str`) vengan poblados en la respuesta, ya que `Model.objects.create()` no los recarga solo.

## Firma

```python
def create_resolucion_directorio(request, payload: ResolucionCreate):
```

## Uso real

`POST /v1/api/resoluciones-directorio/` — response=`InstrumentosLegalesResolucionesOut`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
