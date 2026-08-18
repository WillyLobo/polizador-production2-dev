---
symbol: ComisionadoExternoWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 58-63
signature_hash: sha1:008939fe1821aa1001074f909ff3be52d93fdcb3
authored: true
---

# ComisionadoExternoWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 58-63) · hereda de `AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

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
