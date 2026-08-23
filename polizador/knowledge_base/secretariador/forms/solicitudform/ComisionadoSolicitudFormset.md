---
symbol: ComisionadoSolicitudFormset
kind: class
module: secretariador/forms/solicitudform.py
lines: 136-138
signature_hash: sha1:a524336aff350ab1fa7876b924947f07d8b7c70f
authored: true
---

# ComisionadoSolicitudFormset

**Módulo:** `secretariador/forms/solicitudform.py` (líneas 136-138) · hereda de `forms.models.BaseInlineFormSet`

## Propósito

Formset inline de `ComisionadoSolicitud` sobre una Solicitud del flujo Chaco (`fk_name="comisionadosolicitud_foreign"`, `can_delete=False`). `__init__` sobreescrito sin agregar nada sobre la clase base — vestigial, mismo patrón que varios formsets de `carga`.

## Firma

```python
class ComisionadoSolicitudFormset(forms.models.BaseInlineFormSet):
```

## Uso real

`formset_name = ComisionadoSolicitudFormset` en `CrearSolicitud`/`UpdateSolicitud` (`FormsetViewMixin`).

## Ver también

- [ComisionadoSolicitud](../../models/ComisionadoSolicitud.md)
- [ComisionadoSolicitudForm](ComisionadoSolicitudForm.md)
