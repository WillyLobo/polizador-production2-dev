---
symbol: DetalleCertificado
kind: class
module: carga/views/certificadoviews.py
lines: 369-378
signature_hash: sha1:e2714317e6a738c7fe250f0044f4bdc8cea0f4c4
authored: true
---

# DetalleCertificado

**Módulo:** `carga/views/certificadoviews.py` (líneas 369-378) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de un Certificado (usada también como base para impresión, ver `ImprimirCertificado`), con todo el contexto de `_certificado_detalle_context`.

## Firma

```python
class DetalleCertificado(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`DetalleCertificado` (`carga:detalle-certificado`).

## Ver también

- [_certificado_detalle_context](_certificado_detalle_context.md)
- [ImprimirCertificado](ImprimirCertificado.md)
