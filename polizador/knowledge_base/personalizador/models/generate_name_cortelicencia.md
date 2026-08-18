---
symbol: generate_name_cortelicencia
kind: function
module: personalizador/models.py
lines: 619-624
signature_hash: sha1:2f421c770de7ed39fe393043988b1785f239f650
authored: true
---

# generate_name_cortelicencia

**Módulo:** `personalizador/models.py` (líneas 619-624)

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
