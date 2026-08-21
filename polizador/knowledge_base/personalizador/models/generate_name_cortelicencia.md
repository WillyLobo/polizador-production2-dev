---
symbol: generate_name_cortelicencia
kind: function
module: personalizador/models.py
lines: 746-751
signature_hash: sha1:13bf0346ccfdfc7b8aae76d090a2918c509606be
authored: true
---

# generate_name_cortelicencia

**Módulo:** `personalizador/models.py` (líneas 746-751)

## Propósito

Callback `upload_to` para el adjunto (nota) de un `CorteLicencia`: `licencias/cortes/<cortelicencia_uuid>.<ext>`.

## Firma

```python
def generate_name_cortelicencia(instance, filename):
```

## Uso real

`CorteLicencia.cortelicencia_adjunto` (mismo módulo, más abajo).

## Ver también

- [CorteLicencia](CorteLicencia.md)
