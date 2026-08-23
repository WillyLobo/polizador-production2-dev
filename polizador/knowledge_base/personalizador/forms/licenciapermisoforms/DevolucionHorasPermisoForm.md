---
symbol: DevolucionHorasPermisoForm
kind: class
module: personalizador/forms/licenciapermisoforms.py
lines: 55-67
signature_hash: sha1:1ed609b8bdc488bc9ac8000f88cceef4c41d0a57
authored: true
---

# DevolucionHorasPermisoForm

**Módulo:** `personalizador/forms/licenciapermisoforms.py` (líneas 55-67) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` mínimo para `DevolucionHorasPermiso`: fecha, cantidad de horas, observaciones. Sin lógica propia.

## Firma

```python
class DevolucionHorasPermisoForm(forms.ModelForm):
```

## Uso real

Form base de `DevolucionHorasPermisoFormset`, usado en `CrearLicenciaPermiso`/`UpdateLicenciaPermiso`.

## Ver también

- [DevolucionHorasPermiso](../../models/DevolucionHorasPermiso.md)
