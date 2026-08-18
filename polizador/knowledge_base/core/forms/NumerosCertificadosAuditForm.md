---
symbol: NumerosCertificadosAuditForm
kind: class
module: core/forms.py
lines: 89-90
signature_hash: sha1:32447ff8fc3e7ed0878891b1b52035ee6952a0c4
authored: true
---

# NumerosCertificadosAuditForm

**Módulo:** `core/forms.py` (líneas 89-90) · hereda de `DryRunCheckApplyForm`

## Propósito

Igual que `FixObraResolucionNumbersForm`, sin campos propios más allá de los tres modos heredados.

## Firma

```python
class NumerosCertificadosAuditForm(DryRunCheckApplyForm):
```

## Uso real

`COMMAND_REGISTRY["numeros_certificados_audit"]["form"]`.

## Ver también

- [DryRunCheckApplyForm](DryRunCheckApplyForm.md)
