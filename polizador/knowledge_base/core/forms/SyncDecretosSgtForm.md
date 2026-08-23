---
symbol: SyncDecretosSgtForm
kind: class
module: core/forms.py
lines: 243-281
signature_hash: sha1:a214a3e0f2057e79a1f82d1ae73f545e544b80d1
authored: true
---

# SyncDecretosSgtForm

**Módulo:** `core/forms.py` (líneas 243-281) · hereda de `BaseCommandRunForm`

## Propósito

Mismos campos y mismas exclusiones deliberadas (`--headed`, `--solo-excel`) que `SyncResolucionesSgtForm`, para decretos de licencia en vez de resoluciones.

## Firma

```python
class SyncDecretosSgtForm(BaseCommandRunForm):
```

## Uso real

`COMMAND_REGISTRY["sync_decretos_sgt"]["form"]`.

## Ver también

- [SyncResolucionesSgtForm](SyncResolucionesSgtForm.md)
- [InstrumentosLegalesDecretos](../../../secretariador/models/InstrumentosLegalesDecretos.md)
