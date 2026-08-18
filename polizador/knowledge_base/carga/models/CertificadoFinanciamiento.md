---
symbol: CertificadoFinanciamiento
kind: class
module: carga/models.py
lines: 613-624
signature_hash: sha1:eb304ac3d1a3cc450eea5fd1b359197f42b09d4d
authored: true
---

# CertificadoFinanciamiento

**Módulo:** `carga/models.py` (líneas 613-624) · hereda de `models.Model`

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
