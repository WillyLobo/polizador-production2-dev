---
symbol: ImprimirFojaDeMedicion
kind: class
module: carga/views/fojademedicionviews.py
lines: 280-289
signature_hash: sha1:5cccf251fb8fae6772430ca6ee9ab2dfbb29b854
authored: true
---
# ImprimirFojaDeMedicion

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 280-289) · hereda de `PermissionRequiredMixin, generic.DetailView`

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