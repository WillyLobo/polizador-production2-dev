---
symbol: ImprimirCertificado
kind: class
module: carga/views/certificadoviews.py
lines: 215-225
signature_hash: sha1:0bb50748c462532fbeeb1d91b22172d26e3103bb
authored: true
---

# ImprimirCertificado

**Módulo:** `carga/views/certificadoviews.py` (líneas 215-225) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Mismo template y contexto que `DetalleCertificado`, con `auto_print=True` agregado — el template usa ese flag para disparar el diálogo de impresión del navegador automáticamente al cargar (`window.print()`), en vez de que el usuario tenga que buscar el botón.

## Firma

```python
class ImprimirCertificado(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`ImprimirCertificado` (`carga:imprimir-certificado`).

## Ver también

- [DetalleCertificado](DetalleCertificado.md)
