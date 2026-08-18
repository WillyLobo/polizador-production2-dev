---
symbol: ImprimirFojaDeMedicion
kind: class
module: carga/views/fojademedicionviews.py
lines: 275-284
signature_hash: sha1:7adaca61b415dcdcfa5116395b1b3284e3d77508
authored: true
---

# ImprimirFojaDeMedicion

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 275-284) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Mismo template y contexto que `DetalleFojaDeMedicion`, con `auto_print=True` (mismo patrón que `ImprimirCertificado`).

## Firma

```python
class ImprimirFojaDeMedicion(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`ImprimirFojaDeMedicion` (`carga:imprimir-fojademedicion`).

## Ver también

- [DetalleFojaDeMedicion](DetalleFojaDeMedicion.md)
