---
symbol: CargarTiposLicenciaForm
kind: class
module: core/forms.py
lines: 33-37
signature_hash: sha1:bcb0c2f171a25a9e8f7f137e90d2286baa3ec0b8
authored: true
---

# CargarTiposLicenciaForm

**Módulo:** `core/forms.py` (líneas 33-37) · hereda de `BaseCommandRunForm`

## Propósito

`cargar_tipos_licencia` no toma argumentos: `to_argv()` devuelve `[]`.

## Firma

```python
class CargarTiposLicenciaForm(BaseCommandRunForm):
```

## Uso real

`COMMAND_REGISTRY["cargar_tipos_licencia"]["form"]`.

## Ver también

- [BaseCommandRunForm](BaseCommandRunForm.md)
