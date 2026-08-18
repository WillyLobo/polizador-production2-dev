---
symbol: CrearLicenciaPermiso
kind: class
module: personalizador/views/licenciapermisoviews.py
lines: 27-59
signature_hash: sha1:9834ff0ec6154c592c0825596760ef26c1cf2209
authored: true
---

# CrearLicenciaPermiso

**Módulo:** `personalizador/views/licenciapermisoviews.py` (líneas 27-59) · hereda de `PermissionRequiredMixin, FormsetViewMixin, generic.CreateView`

## Propósito

Alta de LicenciaPermiso junto con su formset inline de `DevolucionHorasPermiso`
(`FormsetViewMixin`). `get_initial` soporta dos entradas por querystring: `?saldo_de_corte=<id>`
precarga agente/tipo desde la licencia original del corte (para registrar un uso parcial
de saldo), y `?agente=<id>` simplemente precarga el agente — mutuamente compatibles con
el flujo normal de carga desde cero.

## Firma

```python
class CrearLicenciaPermiso(PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
```

## Uso real

`CrearLicenciaPermiso` (`personalizador:crear-licenciapermiso`), enlazada desde la ficha de Agente y desde `saldos_pendientes` en `ControlLicenciasAgente`.

## Ver también

- [LicenciaPermiso](../../models/LicenciaPermiso.md)
- [CorteLicencia](../../models/CorteLicencia.md)
