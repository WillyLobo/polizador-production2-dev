---
symbol: DevolucionHorasPermiso
kind: class
module: personalizador/models.py
lines: 704-718
signature_hash: sha1:933a796883f7f939e62b9b557aef0681356496db
authored: true
---

# DevolucionHorasPermiso

**Módulo:** `personalizador/models.py` (líneas 704-718) · hereda de `models.Model`

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
