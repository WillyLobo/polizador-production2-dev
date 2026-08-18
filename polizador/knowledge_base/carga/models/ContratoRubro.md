---
symbol: ContratoRubro
kind: class
module: carga/models.py
lines: 1374-1384
signature_hash: sha1:85ec9d2ec8cacd3078e75b82adff08d80ba06841
authored: true
---

# ContratoRubro

**Módulo:** `carga/models.py` (líneas 1374-1384) · hereda de `models.Model`

## Propósito

**Ojo con el nombre:** este es un tercer concepto de "Rubro" en `carga/models.py`, sin
relación con `CertificadoRubro` ni con `PlanDeTrabajosRubro`. `ContratoRubro` es solo la
categoría de un archivo adjunto de Contrato (`ContratosDigitales.contratodigital_tipo`) —
un catálogo de tipos de documento ("Contrato firmado", "Acta de inicio", etc., según lo
que se haya cargado), no una unidad de obra ni de certificación.

## Firma

```python
class ContratoRubro(models.Model):
```

## Uso real

Referenciado desde `ContratosDigitales.contratodigital_tipo`.

## Ver también

- [ContratosDigitales](ContratosDigitales.md)
- [CertificadoRubro](CertificadoRubro.md) — no confundir.
- [PlanDeTrabajosRubro](PlanDeTrabajosRubro.md) — no confundir.
