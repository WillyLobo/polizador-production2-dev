---
symbol: InstrumentoDecretoLicenciaDependentWidgetMixin
kind: class
module: personalizador/views/ajaxviews.py
lines: 165-183
signature_hash: sha1:b5d7a1d6c7c769e87a6fca8eaf6a26ca66b95b73
authored: true
---

# InstrumentoDecretoLicenciaDependentWidgetMixin

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 165-183)

## Propósito

Acota las opciones de Decreto según el `TipoLicenciaPermiso` elegido en el campo hermano
`licenciapermiso_tipo`: solo tiene sentido filtrar para los dos tipos que un decreto
puede establecer (Anual / Anual de Invierno, comparando por nombre exacto igual que
`personalizador/licencias.py`) — para cualquier otro tipo, no filtra (deja pasar todos
los decretos, ya que no hay una relación conocida que aplicar).

## Firma

```python
class InstrumentoDecretoLicenciaDependentWidgetMixin:
```

## Uso real

`class instrumentodecretowidget(InstrumentoDecretoLicenciaDependentWidgetMixin, ...)`.

## Ver también

- [TipoLicenciaPermiso](../../models/TipoLicenciaPermiso.md)
- [instrumentodecretowidget](instrumentodecretowidget.md)
