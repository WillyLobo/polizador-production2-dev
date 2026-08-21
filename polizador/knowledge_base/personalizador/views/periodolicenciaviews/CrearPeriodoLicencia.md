---
symbol: CrearPeriodoLicencia
kind: class
module: personalizador/views/periodolicenciaviews.py
lines: 21-37
signature_hash: sha1:6b55dedb855c6272cc690f284d74538d209dd22b
authored: true
---

# CrearPeriodoLicencia

**Módulo:** `personalizador/views/periodolicenciaviews.py` (líneas 21-37) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de `PeriodoLicencia` vía `ModelForm` estándar. `get_initial()` precarga
`periodolicencia_categoria`/`periodolicencia_anio` desde querystring (`?categoria=&anio=`)
— es el link que ofrece `ControlLicenciasAgente` cuando el período que le corresponde a
un año todavía no existe.

## Firma

```python
class CrearPeriodoLicencia(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearPeriodoLicencia` (`personalizador:crear-periodolicencia`), enlazada desde
`Lista-periodolicencias.html` y desde `control-licencias.html` cuando falta el período
del año seleccionado.

## Ver también

- [PeriodoLicencia](../../models/PeriodoLicencia.md)
- [PeriodoLicenciaForm](../../forms/periodolicenciaforms/PeriodoLicenciaForm.md)
- [ControlLicenciasAgente](../licenciapermisoviews/ControlLicenciasAgente.md)
