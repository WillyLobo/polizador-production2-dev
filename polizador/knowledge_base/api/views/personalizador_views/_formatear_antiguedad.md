---
symbol: _formatear_antiguedad
kind: function
module: api/views/personalizador_views.py
lines: 697-700
signature_hash: sha1:b011abb2f8829e6ef0a2adef38b37c98152d8037
authored: true
---

# _formatear_antiguedad

**Módulo:** `api/views/personalizador_views.py` (líneas 697-700)

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
