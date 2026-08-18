---
symbol: Uvi
kind: class
module: carga/models.py
lines: 1399-1420
signature_hash: sha1:147afb88e27310bfe2c89ce0297bcd1f4e1e23f1
authored: false
---

# Uvi

**Módulo:** `carga/models.py` (líneas 1399-1420)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class Uvi(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:496` — `return Uvi.pesos_equivalentes(monto_uvi, fecha)`
- `carga/models.py:980` — `pesos = Uvi.pesos_equivalentes(cm.contratomonto_uvi, cm.contratomonto_uvi_fecha)`
- `carga/views/certificadoviews.py:23` — `from carga.models import Certificado, CertificadoFinanciamiento, ContratoMonto, FojaDeMedicion, PlanDeTrabajosEtapa, Uvi`
- `carga/views/certificadoviews.py:60` — `monto_basico_pesos = Uvi.pesos_equivalentes(monto_basico_uvi, certificado.certificado_fecha)`
- `carga/views/certificadoviews.py:61` — `monto_total_pesos = Uvi.pesos_equivalentes(monto_total_uvi, certificado.certificado_fecha)`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
