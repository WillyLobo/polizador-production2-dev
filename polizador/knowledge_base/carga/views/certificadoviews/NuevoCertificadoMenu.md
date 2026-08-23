---
symbol: NuevoCertificadoMenu
kind: class
module: carga/views/certificadoviews.py
lines: 348-350
signature_hash: sha1:4ca8ebfe08727ee9526f1247df2086e63748627f
authored: true
---

# NuevoCertificadoMenu

**Módulo:** `carga/views/certificadoviews.py` (líneas 348-350) · hereda de `PermissionRequiredMixin, generic.TemplateView`

## Propósito

`TemplateView` sin lógica: menú intermedio que enlaza a las distintas formas de crear un Certificado (manual, desde Foja, Anticipo, Hecho Consumado) — un punto de entrada único en vez de que el usuario tenga que saber cuál URL usar.

## Firma

```python
class NuevoCertificadoMenu(PermissionRequiredMixin, generic.TemplateView):
```

## Uso real

`NuevoCertificadoMenu` (`carga:nuevo-certificado-menu`), enlazada desde el navbar ("Obras > Nuevo Certificado").

## Ver también

- [GenerarCertificadosDesdeFoja](GenerarCertificadosDesdeFoja.md)
- [CrearCertificadoAnticipo](CrearCertificadoAnticipo.md)
