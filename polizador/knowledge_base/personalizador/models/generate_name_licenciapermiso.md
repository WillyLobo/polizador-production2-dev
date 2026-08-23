---
symbol: generate_name_licenciapermiso
kind: function
module: personalizador/models.py
lines: 475-481
signature_hash: sha1:84cf199d772709412e2600b8906e3844cfaa35ad
authored: true
---

# generate_name_licenciapermiso

**Módulo:** `personalizador/models.py` (líneas 475-481)

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
