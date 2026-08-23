---
symbol: CorteLicenciaSaldoDependentWidgetMixin
kind: class
module: personalizador/views/ajaxviews.py
lines: 197-209
signature_hash: sha1:1c1f8d3c08a4264175411a5020aaa5ad88308da3
authored: true
---

# CorteLicenciaSaldoDependentWidgetMixin

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 197-209)

## Propósito

Acota las opciones de Corte de Licencia según el Agente elegido en el campo hermano
`licenciapermiso_agente`: solo cortes de ese agente que todavía tengan saldo pendiente
(`corte.dias_restantes > 0`, evaluado en Python fila por fila, no en la query — el
catálogo de cortes por agente es chico, así que no es un problema de performance real).

## Firma

```python
class CorteLicenciaSaldoDependentWidgetMixin:
```

## Uso real

`class cortelicenciawidget(CorteLicenciaSaldoDependentWidgetMixin, ...)`.

## Ver también

- [CorteLicencia](../../models/CorteLicencia.md)
- [cortelicenciawidget](cortelicenciawidget.md)
