---
symbol: SolicitudExteriorForm
kind: class
module: secretariador/forms/solicitud_exteriorform.py
lines: 18-123
signature_hash: sha1:0b9d6e8ff058f4304ca1f89c6bdd1861bafb7abe
authored: true
---

# SolicitudExteriorForm

**Módulo:** `secretariador/forms/solicitud_exteriorform.py` (líneas 18-123) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` para Solicitud fuera del Chaco: sin `solicitud_localidades` (M2M de
localidades del Chaco, no aplica) pero con `solicitud_ciudad` (texto libre) y
`solicitud_aereo` (la variante Exterior sí necesita distinguir traslado aéreo del
terrestre, la Chaco no). `__init__` precarga el último `MontoViaticoDiario` cargado como
default del decreto reglamentario. `clean()` valida que `fecha_hasta >= fecha_desde`.

## Firma

```python
class SolicitudExteriorForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`CrearSolicitudExterior`/`UpdateSolicitudExterior`.

## Ver también

- [Solicitud](../../models/Solicitud.md)
- [SolicitudForm](SolicitudForm.md) — la variante Chaco.
