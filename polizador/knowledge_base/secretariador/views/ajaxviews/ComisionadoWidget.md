---
symbol: ComisionadoWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 52-56
signature_hash: sha1:a6e7741a4ac13c204a3c18e5cddabb90d1b10090
authored: true
---

# ComisionadoWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 52-56) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

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
