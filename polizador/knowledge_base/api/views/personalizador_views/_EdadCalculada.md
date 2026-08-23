---
symbol: _EdadCalculada
kind: class
module: api/views/personalizador_views.py
lines: 690-694
signature_hash: sha1:fa9b1ed2a7cab5114ebcc4a888b2a5f9c3226ef3
authored: true
---

# _EdadCalculada

**Módulo:** `api/views/personalizador_views.py` (líneas 690-694) · hereda de `Func`

## Propósito

Expresión SQL cruda (`models.Func` con `template = "EXTRACT(YEAR FROM AGE(%(expressions)s))"`) que calcula la edad en años completos **en Postgres**, no en Python — para poder ordenar/filtrar el datatable de Agentes por edad sin traer todas las filas a Python primero.

## Firma

```python
class _EdadCalculada(Func):
```

## Uso real

`Agente.objects.annotate(edad_calculada=_EdadCalculada(F('fecha_nacimiento')))`, en el `queryset=` de `register_simple_datatable(router, Agente, "agentes", ...)`.

## Ver también

- [Agente](../../../personalizador/models/Agente.md)
