---
symbol: DecretoWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 74-77
signature_hash: sha1:67968df002000e2bb1a43485c776af7cd53907c0
authored: true
---
# DecretoWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 74-77) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 para elegir un `MontoViaticoDiario`, buscando por la representación textual del decreto reglamentario vinculado.

## Firma

```python
class DecretoWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Solicitud.solicitud_decreto_viaticos` en `SolicitudForm`/`SolicitudExteriorForm`.

## Ver también

- [MontoViaticoDiario](../../models/MontoViaticoDiario.md)