---
symbol: DetalleCertificado
kind: class
module: carga/views/certificadoviews.py
lines: 202-211
signature_hash: sha1:9ea1d4a6a937b429f1961aec8f8d67dd761d6742
authored: true
---

# DetalleCertificado

**Módulo:** `carga/views/certificadoviews.py` (líneas 202-211) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de un Certificado (usada también como base para impresión, ver `ImprimirCertificado`), con todo el contexto de `_certificado_detalle_context` (en `carga/certificado_contexto.py`, compartido con la generación del texto de resolución en `carga/resolucion_texto.py`).

## Firma

```python
class DetalleCertificado(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`DetalleCertificado` (`carga:detalle-certificado`).

## Ver también

- [ImprimirCertificado](ImprimirCertificado.md)
