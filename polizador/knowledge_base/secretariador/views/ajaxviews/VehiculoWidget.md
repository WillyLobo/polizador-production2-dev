---
symbol: VehiculoWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 68-72
signature_hash: sha1:9802a64b555ed01b14ba14e28fd95b141322565c
authored: true
---
# VehiculoWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 68-72) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 para elegir un Vehículo, buscando por modelo y patente.

## Firma

```python
class VehiculoWidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Solicitud.solicitud_vehiculo` en `SolicitudForm`/`SolicitudExteriorForm`; `Vehiculo` en `VehiculoForm` (titular).

## Ver también

- [Vehiculo](../../models/Vehiculo.md)