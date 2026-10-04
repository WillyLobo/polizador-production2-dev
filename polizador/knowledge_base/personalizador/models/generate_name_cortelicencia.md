---
symbol: generate_name_cortelicencia
kind: function
module: personalizador/models.py
lines: 785-790
signature_hash: sha1:84daa058ecf633050da1ecd5f25d6a2e4ffb20b1
authored: true
---

# generate_name_cortelicencia

**Módulo:** `personalizador/models.py` (líneas 785-790)

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
