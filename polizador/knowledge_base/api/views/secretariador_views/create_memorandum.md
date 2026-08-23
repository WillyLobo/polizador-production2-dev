---
symbol: create_memorandum
kind: function
module: api/views/secretariador_views.py
lines: 69-72
signature_hash: sha1:502357110f1455f82efa2554649729e8dea3f1bd
authored: true
---

# create_memorandum

**Módulo:** `api/views/secretariador_views.py` (líneas 69-72)

## Propósito

Alta de `InstrumentosLegalesMemorandum` desde `InstrumentosLegalesMemorandumCreate` (`payload.model_dump()` directo a `InstrumentosLegalesMemorandum.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic). Llama `.refresh_from_db()` después del `create()` — necesario para que los `GeneratedField` calculados por la base (ej. `instrumentolegalresoluciones_str`) vengan poblados en la respuesta, ya que `Model.objects.create()` no los recarga solo.

## Firma

```python
def create_memorandum(request, payload: MemorandumCreate):
```

## Uso real

`POST /v1/api/memorandums/` — response=`InstrumentosLegalesMemorandumOut`.

## Ver también

- [InstrumentosLegalesMemorandum](../../../secretariador/models/InstrumentosLegalesMemorandum.md)
