---
symbol: _EdadCalculada
kind: class
module: api/views/personalizador_views.py
lines: 680-684
signature_hash: sha1:ac3b466ab8a908921198a6a20dde1a1e9304151e
authored: true
---
# _EdadCalculada

**Módulo:** `api/views/personalizador_views.py` (líneas 680-684) · hereda de `Func`

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