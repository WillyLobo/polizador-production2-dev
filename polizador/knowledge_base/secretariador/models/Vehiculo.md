---
symbol: Vehiculo
kind: class
module: secretariador/models.py
lines: 361-401
signature_hash: sha1:43b080552b1f983ad9e88a81adf55dc5a7148a4f
authored: true
---
# Vehiculo

**Módulo:** `secretariador/models.py` (líneas 361-401) · hereda de `models.Model`

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