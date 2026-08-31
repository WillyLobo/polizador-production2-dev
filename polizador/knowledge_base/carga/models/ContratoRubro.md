---
symbol: ContratoRubro
kind: class
module: carga/models.py
lines: 1364-1374
signature_hash: sha1:eb5b97f956bc2b2ea87d23d2bb069bad514e85f7
authored: true
---
# ContratoRubro

**Módulo:** `carga/models.py` (líneas 1364-1374) · hereda de `models.Model`

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