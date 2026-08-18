---
symbol: Vehiculo
kind: class
module: secretariador/models.py
lines: 350-390
signature_hash: sha1:38e8187a3a9d7ade6d4d5f990a8cc3567ca6bd7f
authored: true
---

# Vehiculo

**Módulo:** `secretariador/models.py` (líneas 350-390) · hereda de `models.Model`

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
