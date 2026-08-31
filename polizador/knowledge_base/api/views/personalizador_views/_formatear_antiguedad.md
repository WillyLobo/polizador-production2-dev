---
symbol: _formatear_antiguedad
kind: function
module: api/views/personalizador_views.py
lines: 687-690
signature_hash: sha1:2aaec4834c3ef692cc11fa7550eeaa43f607dd07
authored: true
---
# _formatear_antiguedad

**Módulo:** `api/views/personalizador_views.py` (líneas 687-690)

## Propósito

Formatea el dict `{"anios", "meses", "dias"}` que devuelve `Agente.antiguedad` (property) como texto corto `"Na Nm Nd"` para la columna del datatable.

## Firma

```python
def _formatear_antiguedad(antiguedad: dict | None) -> str:
```

## Uso real

`_agente_datatable_row` (mismo módulo, más abajo).

## Ver también

- [Agente](../../../personalizador/models/Agente.md)
- [_agente_datatable_row](_agente_datatable_row.md)