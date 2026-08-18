---
symbol: LicenciaPermisoForm
kind: class
module: personalizador/forms/licenciapermisoforms.py
lines: 12-53
signature_hash: sha1:153084171f51befcafbb464ec0ebed5204a5fa0b
authored: true
---

# LicenciaPermisoForm

**Módulo:** `personalizador/forms/licenciapermisoforms.py` (líneas 12-53) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` para LicenciaPermiso con todos los widgets dependientes de la sección "Licencias y Permisos" (`agentewidget`, `tipolicenciapermisowidget`, los tres widgets de instrumento legal, `cortelicenciawidget`). Su único `clean()` es una validación liviana de UX (fecha_hasta no anterior a fecha_desde) — deliberadamente redundante con la misma regla en `LicenciaPermiso.clean()` (modelo), para que el error aparezca asociado al campo del formulario en vez de como error general si el usuario llega a saltarse la validación de este form (ej. vía API).

## Firma

```python
class LicenciaPermisoForm(forms.ModelForm):
```

## Uso real

`CrearLicenciaPermiso`/`UpdateLicenciaPermiso` (`personalizador/views/licenciapermisoviews.py`).

## Ver también

- [LicenciaPermiso](../../models/LicenciaPermiso.md)
- [DevolucionHorasPermisoForm](DevolucionHorasPermisoForm.md)
