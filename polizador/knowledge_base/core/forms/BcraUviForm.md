---
symbol: BcraUviForm
kind: class
module: core/forms.py
lines: 40-55
signature_hash: sha1:1817cfe15f269591242ca60e0508f78f12487fef
authored: true
---

# BcraUviForm

**Módulo:** `core/forms.py` (líneas 40-55) · hereda de `BaseCommandRunForm`

## Propósito

Un solo campo (`full_sync`, checkbox): tildado agrega `--full-sync` (descarga toda la serie histórica del BCRA, ignorando lo ya guardado — los duplicados se saltean); sin tildar, el comando por defecto solo trae valores nuevos desde el último registrado.

## Firma

```python
class BcraUviForm(BaseCommandRunForm):
```

## Uso real

`COMMAND_REGISTRY["bcra_uvi"]["form"]`.

## Ver también

- [Uvi](../../../carga/models/Uvi.md)
