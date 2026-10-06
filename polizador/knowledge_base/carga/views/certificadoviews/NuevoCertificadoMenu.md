---
symbol: NuevoCertificadoMenu
kind: class
module: carga/views/certificadoviews.py
lines: 181-183
signature_hash: sha1:4bf651959b08bce36cab08bc8ee4edac01a04cfa
authored: true
---

# NuevoCertificadoMenu

**Módulo:** `carga/views/certificadoviews.py` (líneas 181-183) · hereda de `PermissionRequiredMixin, generic.TemplateView`

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
