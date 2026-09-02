---
symbol: Vehiculo
kind: class
module: secretariador/models.py
lines: 360-400
signature_hash: sha1:ccb2e923bd42c9612327a624fe3bf786d45d4e5a
authored: true
---
# Vehiculo

**Módulo:** `secretariador/models.py` (líneas 360-400) · hereda de `models.Model`

## Propósito

Un vehículo (de la empresa, oficial, o particular) disponible para comisiones de servicio, con su titular (Agente o Empresa, ambos opcionales) y datos de póliza. `save()` normaliza la patente sacándole espacios (`"AB 123 CD"` → `"AB123CD"`) antes de guardar, para que las búsquedas/comparaciones no dependan de cómo lo tipeó el usuario.

## Firma

```python
class Vehiculo(models.Model):
```

## Uso real

`Solicitud.solicitud_vehiculo` en `SolicitudForm`/`SolicitudExteriorForm` (vía `VehiculoWidget`).

## Ver también

- [Solicitud](Solicitud.md)