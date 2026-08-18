---
symbol: format_thousands
kind: function
module: api/views/generics.py
lines: 70-74
signature_hash: sha1:c1f35e1525bc4fe560e6061e8e6e9802178bc989
authored: true
---

# format_thousands

**Módulo:** `api/views/generics.py` (líneas 70-74)

## Propósito

Formatea un número con "." como separador de miles y "," como marca decimal (convención es-AR), replicando `locale.format_string("%.2f", value, True)` de los `AjaxDatatableView` legados **sin tocar el locale del proceso** (que es global y compartido entre requests — cambiar el locale del proceso para un solo request sería una condición de carrera entre requests concurrentes).

## Firma

```python
def format_thousands(value) -> str:
```

## Uso real

`_obra_ext_datatable_row`, `_certificado_datatable_row` (montos).

## Ver también

_(sin referencias cruzadas)_
