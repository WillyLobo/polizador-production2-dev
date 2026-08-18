---
symbol: FojaDeMedicionFoto
kind: class
module: carga/models.py
lines: 1269-1280
signature_hash: sha1:f89ad6b580b0427b30284611b1b80ff77873d92b
authored: true
---

# FojaDeMedicionFoto

**Módulo:** `carga/models.py` (líneas 1269-1280) · hereda de `models.Model`

## Propósito

Foto adjunta (evidencia fotográfica) de una Foja de Medición — a diferencia de los otros adjuntos del módulo, acepta imagen (jpeg/png), no PDF.

## Firma

```python
class FojaDeMedicionFoto(models.Model):
```

## Uso real

Formset inline dentro de `CrearFojaDeMedicion`/`UpdateFojaDeMedicion` (`carga/views/fojademedicionviews.py:146,234`, `foto_formset.save()`).

## Ver también

- [FojaDeMedicion](FojaDeMedicion.md)
