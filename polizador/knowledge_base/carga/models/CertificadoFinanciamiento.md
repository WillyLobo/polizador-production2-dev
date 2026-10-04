---
symbol: CertificadoFinanciamiento
kind: class
module: carga/models.py
lines: 706-717
signature_hash: sha1:7d48486e329e8e4ea5fc19920b918f7f714ef8cf
authored: true
---

# CertificadoFinanciamiento

**Módulo:** `carga/models.py` (líneas 706-717) · hereda de `models.Model`

## Propósito

Catálogo normalizado de fuentes de financiamiento (Nación/Provincia/Terceros), con
`_nombre_corto` de un carácter (N/P/T) — el mismo código corto que usan
`Certificado.FINANCIAMIENTO` (todavía un `CharField` de choices, sin migrar a FK) y
`Obra.recalcular_montos_contrato()` para agrupar montos.

## Firma

```python
class CertificadoFinanciamiento(models.Model):
```

## Uso real

Referenciado desde `ContratoMonto.contratomonto_financiamiento`.

## Ver también

- [ContratoMonto](ContratoMonto.md)
- [Certificado](Certificado.md)
