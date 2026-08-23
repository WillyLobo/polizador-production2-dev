---
symbol: DetalleFojaDeMedicion
kind: class
module: carga/views/fojademedicionviews.py
lines: 263-271
signature_hash: sha1:7345564d6ebd1415273d98a7f1293fd6d321515d
authored: true
---

# DetalleFojaDeMedicion

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 263-271) · hereda de `PermissionRequiredMixin, generic.DetailView`

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
