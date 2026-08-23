---
symbol: FixObraResolucionNumbersForm
kind: class
module: core/forms.py
lines: 83-86
signature_hash: sha1:3460ec8fb86d7d56dc1412ddfa115ed28363ab0f
authored: true
---

# FixObraResolucionNumbersForm

**Módulo:** `core/forms.py` (líneas 83-86) · hereda de `DryRunCheckApplyForm`

## Propósito

Usa los tres modos de `DryRunCheckApplyForm` sin agregar campos propios — deliberadamente no expone `--output` (ruta de archivo libre) para no aceptar una ruta arbitraria del lado del servidor.

## Firma

```python
class FixObraResolucionNumbersForm(DryRunCheckApplyForm):
```

## Uso real

`COMMAND_REGISTRY["fix_obra_resolucion_numbers"]["form"]`.

## Ver también

- [DryRunCheckApplyForm](DryRunCheckApplyForm.md)
