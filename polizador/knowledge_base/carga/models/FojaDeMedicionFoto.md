---
symbol: FojaDeMedicionFoto
kind: class
module: carga/models.py
lines: 1527-1538
signature_hash: sha1:244abf812117dddb3446a18c52dc17f7b92d27d7
authored: true
---
# FojaDeMedicionFoto

**Módulo:** `carga/models.py` (líneas 1527-1538) · hereda de `models.Model`

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