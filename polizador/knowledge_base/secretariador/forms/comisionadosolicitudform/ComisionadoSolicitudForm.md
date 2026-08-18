---
symbol: ComisionadoSolicitudForm
kind: class
module: secretariador/forms/comisionadosolicitudform.py
lines: 12-84
signature_hash: sha1:41e57bf78fed4ea6f0722ac5f895f7ecd902b7ab
authored: true
---

# ComisionadoSolicitudForm

**Módulo:** `secretariador/forms/comisionadosolicitudform.py` (líneas 12-84) · hereda de `AddRelatedPermissionMixin, BaseFormMixin, forms.ModelForm`

## Propósito

Misma estructura y misma validación `clean()` que `ComisionadoSolicitudExteriorForm` (elegir exactamente uno de Agente/Externo, sin duplicar la fecha), pero sin el campo `comisionadosolicitud_pasaje` — la variante del flujo Chaco (viáticos dentro de la provincia, donde no aplica pasaje aéreo/terrestre de larga distancia). Usa `AddRelatedPermissionMixin` (de `carga.forms.mixins`, reusado entre apps) para ocultar los botones "+" de sus widgets según permisos.

## Firma

```python
class ComisionadoSolicitudForm(AddRelatedPermissionMixin, BaseFormMixin, forms.ModelForm):
```

## Uso real

Form base de `ComisionadoSolicitudFormset` (`solicitudform.py`) y de `ComisionadoIncorporacionFormset` (`incorporacionform.py`, sin subclase propia).

## Ver también

- [ComisionadoSolicitud](../../models/ComisionadoSolicitud.md)
- [ComisionadoSolicitudExteriorForm](ComisionadoSolicitudExteriorForm.md)
