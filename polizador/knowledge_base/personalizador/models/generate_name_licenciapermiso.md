---
symbol: generate_name_licenciapermiso
kind: function
module: personalizador/models.py
lines: 514-520
signature_hash: sha1:7b8996ba44cc6973b62a06ad06c10adc66601985
authored: true
---

# generate_name_licenciapermiso

**Módulo:** `personalizador/models.py` (líneas 514-520)

## Propósito

Callback `upload_to` para el adjunto de una `LicenciaPermiso` (certificado/comunicación): `licencias/adjuntos/<licenciapermiso_uuid>.<ext>`, preservando la extensión original.

## Firma

```python
def generate_name_licenciapermiso(instance, filename):
```

## Uso real

`LicenciaPermiso.licenciapermiso_adjunto` (mismo módulo, más abajo).

## Ver también

- [LicenciaPermiso](LicenciaPermiso.md)
