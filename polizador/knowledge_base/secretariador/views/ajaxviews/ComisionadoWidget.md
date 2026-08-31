---
symbol: ComisionadoWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 52-59
signature_hash: sha1:91eafd08759779431f3888b9a76d0c1da3202ac8
authored: true
---
# ComisionadoWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 52-59) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 para elegir un Agente en su rol de "comisionado" (nombres/apellidos) — mismo `search_fields` que `carga.views.ajaxviews.agentewidget`/`personalizador.views.ajaxviews.agentewidget`, redefinido acá en vez de reusar uno de esos dos.

## Firma

```python
class ComisionadoWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Solicitud.solicitud_solicitante`, `ComisionadoSolicitud.comisionadosolicitud_nombre`, `Vehiculo.vehiculo_titular_agente`, `Incorporacion.incorporacion_solicitante` en varios forms de `secretariador`.

## Ver también

- [ComisionadoSolicitud](../../models/ComisionadoSolicitud.md)