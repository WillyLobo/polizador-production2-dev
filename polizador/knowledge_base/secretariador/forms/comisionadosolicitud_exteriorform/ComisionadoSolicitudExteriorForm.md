---
symbol: ComisionadoSolicitudExteriorForm
kind: class
module: secretariador/forms/comisionadosolicitud_exteriorform.py
lines: 8-86
signature_hash: sha1:c04f60058510d8157cd685ab4d586b604f6e6f5b
authored: true
---

# ComisionadoSolicitudExteriorForm

**Módulo:** `secretariador/forms/comisionadosolicitud_exteriorform.py` (líneas 8-86) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` para `ComisionadoSolicitud`, variante para el flujo Exterior (incluye
`comisionadosolicitud_pasaje`, que la variante estándar no tiene expuesto en este form —
ver `ComisionadoSolicitudForm`). `clean()` valida que se haya elegido exactamente uno de
Agente/Externo (redundante con el `CheckConstraint` del modelo, para dar el error
asociado al campo del formulario) y que esa persona no esté ya comisionada en **otra**
Solicitud con las mismas fechas exactas (`solicitud_fecha_desde`/`solicitud_fecha_hasta`,
leídos de `self.data` — no de otro campo del propio form, ya que pertenecen al form padre
`Solicitud`, no al formset de comisionados) — salvo que esa otra Solicitud esté anulada.

## Firma

```python
class ComisionadoSolicitudExteriorForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

Form base de `ComisionadoSolicitudExteriorFormset` (definido con `inlineformset_factory` en `solicitud_exteriorform.py`, sin subclase propia — por eso no aparece como símbolo aparte en este manifest).

## Ver también

- [ComisionadoSolicitud](../../models/ComisionadoSolicitud.md)
- [ComisionadoSolicitudForm](ComisionadoSolicitudForm.md) — misma validación, para el flujo Chaco.
