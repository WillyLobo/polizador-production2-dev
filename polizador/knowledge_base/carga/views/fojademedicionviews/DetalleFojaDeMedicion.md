---
symbol: DetalleFojaDeMedicion
kind: class
module: carga/views/fojademedicionviews.py
lines: 268-276
signature_hash: sha1:490414939f927e89342a1ff7f6c390026e8707b5
authored: true
---
# DetalleFojaDeMedicion

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 268-276) · hereda de `PermissionRequiredMixin, generic.DetailView`

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