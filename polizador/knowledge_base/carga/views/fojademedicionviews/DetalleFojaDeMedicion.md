---
symbol: DetalleFojaDeMedicion
kind: class
module: carga/views/fojademedicionviews.py
lines: 265-273
signature_hash: sha1:32e7eebcf48470ff794cc148726cb75775f21d2d
authored: true
---
# DetalleFojaDeMedicion

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 265-273) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de una Foja (base también de la impresión), con el contexto de `_foja_detalle_context`.

## Firma

```python
class DetalleFojaDeMedicion(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`DetalleFojaDeMedicion` (`carga:detalle-fojademedicion`).

## Ver también

- [_foja_detalle_context](_foja_detalle_context.md)
- [ImprimirFojaDeMedicion](ImprimirFojaDeMedicion.md)