---
symbol: create_obra
kind: function
module: api/views/carga_views.py
lines: 774-788
signature_hash: sha1:0cd4b2d5094dd2c876e38882a6e7e9a1760ab6f8
authored: true
---

# create_obra

**Módulo:** `api/views/carga_views.py` (líneas 774-788)

## Propósito

Alta de Obra con manejo explícito de los cuatro M2M (`departamento_ids`/`municipio_ids`/
`localidad_ids`/`inspector_ids`): se los saca del payload antes de `Obra.objects.create()`
(un M2M no se puede pasar a `create()`, la instancia todavía no tiene PK) y se asignan
después con `.set()` sobre la instancia ya creada.

## Firma

```python
def create_obra(request, payload: ObraCreate):
```

## Uso real

`POST /v1/api/obras/` — response=`ObraOut` (vía `_obra_out`).

## Ver también

- [Obra](../../../carga/models/Obra.md)
- [_obra_out](_obra_out.md)
