---
symbol: TipoLicenciaPermisoForm
kind: class
module: personalizador/forms/tipolicenciapermisoforms.py
lines: 4-36
signature_hash: sha1:cf3789e260e7eb437d7f3b5f12ba26ae1f5ea0d6
authored: true
---

# TipoLicenciaPermisoForm

**Módulo:** `personalizador/forms/tipolicenciapermisoforms.py` (líneas 4-36) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para `TipoLicenciaPermiso`: expone toda la parametrización del tipo (unidad, tope, período del tope, si es remunerada, antigüedad mínima, si requiere certificado/compensación horaria). Sin `clean()` propio.

## Firma

```python
class TipoLicenciaPermisoForm(forms.ModelForm):
```

## Uso real

`CrearTipoLicenciaPermiso`/`UpdateTipoLicenciaPermiso` — en la práctica el catálogo se carga vía management command, este form es más para ajustes puntuales.

## Ver también

- [TipoLicenciaPermiso](../../models/TipoLicenciaPermiso.md)
