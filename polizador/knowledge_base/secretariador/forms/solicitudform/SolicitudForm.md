---
symbol: SolicitudForm
kind: class
module: secretariador/forms/solicitudform.py
lines: 20-134
signature_hash: sha1:7ff3017c6d72454ce986668d31021d08ddfd3bbd
authored: true
---

# SolicitudForm

**Módulo:** `secretariador/forms/solicitudform.py` (líneas 20-134) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` para Solicitud dentro del Chaco: incluye `solicitud_localidades` (M2M, con
`localidadmultiplewidget` de `carga`) en vez de `solicitud_ciudad`/`solicitud_aereo` de
la variante Exterior. `__init__` precarga el último `MontoViaticoDiario` como decreto por
defecto y la Provincia del Chaco (`pk=22`) como default de `solicitud_provincia`. Mismo
`clean()` de fechas que `SolicitudExteriorForm`.

## Firma

```python
class SolicitudForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`CrearSolicitud`/`UpdateSolicitud` (`secretariador/views/solicitudviews.py`).

## Ver también

- [Solicitud](../../models/Solicitud.md)
- [SolicitudExteriorForm](SolicitudExteriorForm.md)
