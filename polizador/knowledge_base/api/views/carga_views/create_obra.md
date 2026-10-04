---
symbol: create_obra
kind: function
module: api/views/carga_views.py
lines: 775-789
signature_hash: sha1:2b98f95d18da3fe550dac294fd4c40885f336ea3
authored: true
---

# create_obra

**Módulo:** `api/views/carga_views.py` (líneas 775-789)

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
