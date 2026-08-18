---
symbol: IncorporacionForm
kind: class
module: secretariador/forms/incorporacionform.py
lines: 11-41
signature_hash: sha1:616bfaf6d93698caaf3df42e02444f95d850fce9
authored: true
---

# IncorporacionForm

**Módulo:** `secretariador/forms/incorporacionform.py` (líneas 11-41) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` para Incorporación: la Solicitud a la que se incorpora (widget de búsqueda), datos de la nueva actuación, solicitante y resolución. Sin `clean()` propio.

## Firma

```python
class IncorporacionForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`CrearIncorporacion`/`UpdateIncorporacion` (`secretariador/views/incorporacionviews.py`).

## Ver también

- [Incorporacion](../../models/Incorporacion.md)
