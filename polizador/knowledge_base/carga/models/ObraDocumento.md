---
symbol: ObraDocumento
kind: class
module: carga/models.py
lines: 654-667
signature_hash: sha1:528ecb713fd5aeec8731e152b53cb639fcf577bc
authored: true
---

# ObraDocumento

**Módulo:** `carga/models.py` (líneas 654-667) · hereda de `models.Model`

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
