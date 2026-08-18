---
symbol: SolicitudWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 47-50
signature_hash: sha1:0cd9c5eb9f01434b14c543ff297c5826e6bb590a
authored: true
---

# SolicitudWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 47-50) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 para elegir una Solicitud, buscando por su actuación electrónica.

## Firma

```python
class SolicitudWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Incorporacion.incorporacion_solicitud` en `IncorporacionForm`.

## Ver también

- [Solicitud](../../models/Solicitud.md)
