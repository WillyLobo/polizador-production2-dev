---
symbol: CertificadoFinanciamiento
kind: class
module: carga/models.py
lines: 613-624
signature_hash: sha1:eb304ac3d1a3cc450eea5fd1b359197f42b09d4d
authored: false
---

# CertificadoFinanciamiento

**Módulo:** `carga/models.py` (líneas 613-624)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class CertificadoFinanciamiento(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:1365` — `contratomonto_financiamiento = models.ForeignKey("CertificadoFinanciamiento", verbose_name="Financiamiento", on_delete=models.CASCADE)`
- `carga/views/certificadoviews.py:23` — `from carga.models import Certificado, CertificadoFinanciamiento, ContratoMonto, FojaDeMedicion, PlanDeTrabajosEtapa, Uvi`
- `carga/views/certificadoviews.py:84` — `financiamiento = CertificadoFinanciamiento.objects.filter(`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
