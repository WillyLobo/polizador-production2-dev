---
symbol: ControlLicenciasAgente
kind: function
module: personalizador/views/licenciapermisoviews.py
lines: 99-115
signature_hash: sha1:af7aa831c83aa48adb2c991b56ea2385721fba37
authored: true
---

# ControlLicenciasAgente

**Módulo:** `personalizador/views/licenciapermisoviews.py` (líneas 99-115)

## Propósito

El panel de control de licencias de un Agente para un año dado (`?anio=`, default el año
actual, con un selector de los últimos 5 años + el actual): combina
`personalizador.licencias.resumen_agente` (balance correspondientes/usados/disponibles de
cada `TipoLicenciaPermiso` activo) con `saldos_pendientes_agente` (cortes con saldo aún no
vencido) en una sola pantalla — es la vista que le da uso real a toda la lógica de cálculo
de `personalizador/licencias.py`.

Además resuelve (sin crear) el [PeriodoLicencia](../../models/PeriodoLicencia.md) `LOR_ANUAL`
y `LOR_INVIERNO` del año seleccionado (`get_periodo`) y los pasa al contexto: el template
muestra su apertura/límite de solicitud (o turnos, para Invierno), y si alguno todavía no
existe ofrece un link a `crear-periodolicencia` con la categoría/año precargados por
querystring.

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
- [PeriodoLicencia](../../models/PeriodoLicencia.md)
- [CrearPeriodoLicencia](../periodolicenciaviews/CrearPeriodoLicencia.md)
