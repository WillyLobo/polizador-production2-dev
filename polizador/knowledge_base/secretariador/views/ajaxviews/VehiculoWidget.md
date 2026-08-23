---
symbol: VehiculoWidget
kind: class
module: secretariador/views/ajaxviews.py
lines: 65-69
signature_hash: sha1:3a749ac75f2de47b77bb29f5292eaa0198f072ab
authored: true
---

# VehiculoWidget

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 65-69) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

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
