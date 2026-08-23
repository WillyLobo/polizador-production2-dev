---
symbol: DryRunCheckApplyForm
kind: class
module: core/forms.py
lines: 58-80
signature_hash: sha1:412643a831e72f39bc03dc89abdd6544dd71afe2
authored: true
---

# DryRunCheckApplyForm

**Módulo:** `core/forms.py` (líneas 58-80) · hereda de `BaseCommandRunForm`

## Propósito

Base reusable para comandos con tres modos mutuamente excluyentes (radio buttons, no checkboxes independientes): chequeo de solo lectura (preseleccionado, el más seguro), simulación detallada, o aplicar los cambios de verdad. `to_argv()` traduce el modo elegido al flag correspondiente (`--check`/`--dry-run`/nada para aplicar).

## Firma

```python
class DryRunCheckApplyForm(BaseCommandRunForm):
```

## Uso real

Superclase de `FixObraResolucionNumbersForm`/`NumerosCertificadosAuditForm`.

## Ver también

- [BaseCommandRunForm](BaseCommandRunForm.md)
- [FixObraResolucionNumbersForm](FixObraResolucionNumbersForm.md)
