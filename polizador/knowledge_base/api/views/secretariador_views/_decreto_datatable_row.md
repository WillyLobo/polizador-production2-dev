---
symbol: _decreto_datatable_row
kind: function
module: api/views/secretariador_views.py
lines: 246-266
signature_hash: sha1:ae8ea31337961c0ac67a46bdea28c79b4919aa37
authored: true
---

# _decreto_datatable_row

**Módulo:** `api/views/secretariador_views.py` (líneas 246-266)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila que consume el datatable JS — datos ya formateados a texto/HTML más una columna `acciones` con los links editar/detalle/eliminar, cada uno mostrado solo si `user.has_perm(...)` correspondiente. Incluye `instrumentolegaldecretos_es_licencia`, un campo que no existe en el modelo — viene de la anotación `_DECRETOS_QUERYSET` (mismo módulo) que unifica los dos flags `establece_licencia_anual`/`establece_licencia_invierno` en un solo booleano.

## Firma

```python
def _decreto_datatable_row(d: InstrumentosLegalesDecretos, user) -> dict:
```

## Uso real

`register_simple_datatable(router, InstrumentosLegalesDecretos, "decretos", ..., queryset=_DECRETOS_QUERYSET)`.

## Ver también

- [InstrumentosLegalesDecretos](../../../secretariador/models/InstrumentosLegalesDecretos.md)
