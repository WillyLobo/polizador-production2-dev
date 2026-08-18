---
symbol: _poliza_datatable_row
kind: function
module: api/views/carga_views.py
lines: 1845-1871
signature_hash: sha1:65376be2c49e392b8da602f7cdae80e6e52f13b6
authored: true
---

# _poliza_datatable_row

**Módulo:** `api/views/carga_views.py` (líneas 1845-1871)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Incluye una columna `poliza_editor` **siempre vacía**, con un comentario explícito en el código: es una columna heredada del `AjaxDatatableView` original que nunca se llegó a completar (`poliza_editor` no es un campo real del modelo) — se preserva vacía a propósito para no alterar el comportamiento previo al migrar a este endpoint, no es un bug nuevo introducido acá.

## Firma

```python
def _poliza_datatable_row(p: Poliza, user) -> dict:
```

## Uso real

`row_builder` de `register_simple_datatable(router, Poliza, "polizas", ...)`.

## Ver también

- [Poliza](../../../carga/models/Poliza.md)
