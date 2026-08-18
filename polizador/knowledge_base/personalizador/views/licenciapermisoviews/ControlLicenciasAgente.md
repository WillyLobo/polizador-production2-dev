---
symbol: ControlLicenciasAgente
kind: function
module: personalizador/views/licenciapermisoviews.py
lines: 99-113
signature_hash: sha1:f293d78b44f263407b7d74e4156087165817c647
authored: true
---

# ControlLicenciasAgente

**Módulo:** `personalizador/views/licenciapermisoviews.py` (líneas 99-113)

## Propósito

El panel de control de licencias de un Agente para un año dado (`?anio=`, default el año
actual, con un selector de los últimos 5 años + el actual): combina
`personalizador.licencias.resumen_agente` (balance correspondientes/usados/disponibles de
cada `TipoLicenciaPermiso` activo) con `saldos_pendientes_agente` (cortes con saldo aún no
vencido) en una sola pantalla — es la vista que le da uso real a toda la lógica de cálculo
de `personalizador/licencias.py`.

## Firma

```python
def ControlLicenciasAgente(request, pk):
```

## Uso real

`ControlLicenciasAgente` (`personalizador:control-licencias-agente`), enlazada desde `FichaAgente`.

## Ver también

- [FichaAgente](../agenteviews/FichaAgente.md)
- [LicenciaPermiso](../../models/LicenciaPermiso.md)
- [TipoLicenciaPermiso](../../models/TipoLicenciaPermiso.md)
