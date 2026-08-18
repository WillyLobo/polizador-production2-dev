---
symbol: CheckResolucionesForm
kind: class
module: core/forms.py
lines: 26-30
signature_hash: sha1:440bd6088f8f80ba4abe2bbc3f118541dd930880
authored: true
---

# CheckResolucionesForm

**Módulo:** `core/forms.py` (líneas 26-30) · hereda de `BaseCommandRunForm`

## Propósito

`resolucion_audit` no toma argumentos: `to_argv()` devuelve `[]`.

## Firma

```python
class CheckResolucionesForm(BaseCommandRunForm):
```

## Uso real

`COMMAND_REGISTRY["resolucion_audit"]["form"]`.

## Ver también

- [BaseCommandRunForm](BaseCommandRunForm.md)
