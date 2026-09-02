---
symbol: ImprimirFojaDeMedicion
kind: class
module: carga/views/fojademedicionviews.py
lines: 277-286
signature_hash: sha1:315111725cf7b8935d92fc940d81c4f5450a492c
authored: true
---
# ImprimirFojaDeMedicion

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 277-286) · hereda de `PermissionRequiredMixin, generic.DetailView`

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