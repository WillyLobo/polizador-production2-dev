---
symbol: VehiculoForm
kind: class
module: secretariador/forms/vehiculoform.py
lines: 12-58
signature_hash: sha1:c507477994c4890336642366675b8d1b236f4604
authored: true
---

# VehiculoForm

**Módulo:** `secretariador/forms/vehiculoform.py` (líneas 12-58) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` estándar para Vehículo: designación (Empresa/Oficial/Particular), datos de póliza (`aseguradorawidget` de `carga`), titular (Agente vía `ComisionadoWidget` o Empresa vía `empresawidget` de `carga`, ambos opcionales — no hay una regla de exclusividad como en `ComisionadoSolicitud`).

## Firma

```python
class VehiculoForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`CrearVehiculo`/`UpdateVehiculo` (`secretariador/views/vehiculoviews.py`).

## Ver también

- [Vehiculo](../../models/Vehiculo.md)
