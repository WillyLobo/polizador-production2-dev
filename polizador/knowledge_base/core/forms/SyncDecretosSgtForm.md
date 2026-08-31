---
symbol: SyncDecretosSgtForm
kind: class
module: core/forms.py
lines: 250-288
signature_hash: sha1:66e2438f70362ae388cda04d2a90876e3bbbe45e
authored: true
---
# SyncDecretosSgtForm

**Módulo:** `core/forms.py` (líneas 250-288) · hereda de `BaseCommandRunForm`

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