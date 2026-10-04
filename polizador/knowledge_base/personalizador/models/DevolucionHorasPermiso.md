---
symbol: DevolucionHorasPermiso
kind: class
module: personalizador/models.py
lines: 870-884
signature_hash: sha1:ab23e551e659867ca030f3e9ce3e43a22d7f33c9
authored: true
---

# DevolucionHorasPermiso

**Módulo:** `personalizador/models.py` (líneas 870-884) · hereda de `models.Model`

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
