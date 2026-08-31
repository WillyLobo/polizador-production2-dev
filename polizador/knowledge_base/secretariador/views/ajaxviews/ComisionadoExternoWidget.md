---
symbol: ComisionadoExternoWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 61-66
signature_hash: sha1:dfa9c6cc30ef6040e2abcad072732b7d125bfe76
authored: true
---
# ComisionadoExternoWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 61-66) · hereda de `AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 para elegir un `ComisionadoExterno`, con alta rápida (`AddRelatedWidgetMixin` → `secretariador:crear-comisionado-externo`).

## Firma

```python
class ComisionadoExternoWidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`ComisionadoSolicitud.comisionadosolicitud_externo` en `ComisionadoSolicitudForm`/`ComisionadoSolicitudExteriorForm`.

## Ver también

- [ComisionadoSolicitud](../../models/ComisionadoSolicitud.md)