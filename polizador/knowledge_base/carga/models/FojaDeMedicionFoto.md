---
symbol: FojaDeMedicionFoto
kind: class
module: carga/models.py
lines: 1259-1270
signature_hash: sha1:0c27df1b1f5866f96f5d49d066e437493f381397
authored: true
---
# FojaDeMedicionFoto

**Módulo:** `carga/models.py` (líneas 1259-1270) · hereda de `models.Model`

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