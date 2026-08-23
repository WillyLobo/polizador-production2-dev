---
symbol: parse_order_by
kind: function
module: api/views/generics.py
lines: 46-56
signature_hash: sha1:052e0cfb2cd9f222c8f245ccf6674a345dc75d6e
authored: true
---

# parse_order_by

**Módulo:** `api/views/generics.py` (líneas 46-56)

## Propósito

Traduce el string `order_by` que manda `ninja-datatable.js` (columnas separadas por coma, prefijo `-` para descendente) a una lista de argumentos de `.order_by()` de Django, mapeando cada clave de columna a un campo real vía `fields_map` (con `default_field` de fallback si la clave no está mapeada).

## Firma

```python
def parse_order_by(order_by: str, fields_map: dict, default_field: str='id') -> list:
```

## Uso real

Todos los endpoints `datatable_*` a mano (no `register_simple_datatable`, que ya lo llama internamente): `datatable_obras`, `datatable_certificados`, `datatable_solicitudes`, etc.

## Ver también

- [register_simple_datatable](register_simple_datatable.md)
