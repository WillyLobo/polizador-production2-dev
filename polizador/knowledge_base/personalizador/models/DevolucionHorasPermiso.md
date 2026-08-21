---
symbol: DevolucionHorasPermiso
kind: class
module: personalizador/models.py
lines: 831-845
signature_hash: sha1:f6d8e331f88fdcf3b37c7f9f7d9c4817a8a3d78e
authored: true
---

# DevolucionHorasPermiso

**Módulo:** `personalizador/models.py` (líneas 831-845) · hereda de `models.Model`

## Propósito

Registro de horas devueltas por un agente para compensar un permiso que la ley obliga a devolver con horas de trabajo (ej. razones particulares, lactancia — ver `TipoLicenciaPermiso.tipolicenciapermiso_compensacion_horaria`). Un `LicenciaPermiso` puede tener varias devoluciones parciales (`related_name="devolucionhoras_set"`).

## Firma

```python
class DevolucionHorasPermiso(models.Model):
```

## Uso real

Formset inline (`DevolucionHorasPermisoFormset`) dentro de `CrearLicenciaPermiso`/`UpdateLicenciaPermiso`.

## Ver también

- [LicenciaPermiso](LicenciaPermiso.md)
