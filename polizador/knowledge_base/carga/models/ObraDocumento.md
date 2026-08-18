---
symbol: ObraDocumento
kind: class
module: carga/models.py
lines: 561-574
signature_hash: sha1:190e281de9602b71244f4a0cb4c8a3632f2df06c
authored: true
---

# ObraDocumento

**Módulo:** `carga/models.py` (líneas 561-574) · hereda de `models.Model`

## Propósito

Documento PDF adjunto a una Obra (genérico — sin tipo/categoría propia, a diferencia de `ContratosDigitales` que sí tiene `contratodigital_tipo`).

## Firma

```python
class ObraDocumento(models.Model):
```

## Uso real

`ObraDocumentoForm` (buscar en `carga/forms/`), asociada a `Obra.documentos_obra` (related_name).

## Ver también

- [Obra](Obra.md)
