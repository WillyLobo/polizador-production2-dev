---
symbol: create_gerencia
kind: function
module: api/views/personalizador_views.py
lines: 62-63
signature_hash: sha1:f37e3abde13607991d07b9f18e25eddf02d5a8be
authored: true
---

# create_gerencia

**Módulo:** `api/views/personalizador_views.py` (líneas 62-63)

## Propósito

Alta de `Gerencia` desde `GerenciaCreate` (`payload.model_dump()` directo a `Gerencia.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_gerencia(request, payload: GerenciaCreate):
```

## Uso real

`POST /v1/api/gerencias/` — response=`GerenciaOut`.

## Ver también

- [Gerencia](../../../personalizador/models/Gerencia.md)
