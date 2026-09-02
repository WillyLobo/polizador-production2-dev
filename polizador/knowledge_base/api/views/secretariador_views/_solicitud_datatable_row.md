---
symbol: _solicitud_datatable_row
kind: function
module: api/views/secretariador_views.py
lines: 655-696
signature_hash: sha1:d4631de90e5806affcf759a89e98add90404bd4f
authored: true
---
# _solicitud_datatable_row

**Módulo:** `api/views/secretariador_views.py` (líneas 655-696)

## Propósito

El row-builder más elaborado del módulo: el link de editar/eliminar/generar-documento
bifurca según `solicitud_provincia` (Chaco vs. Exterior van a URLs de vista distintas —
mismo patrón de bifurcación que `Solicitud.get_absolute_url()`, ver la página del
modelo); el link de detalle muestra el PDF de la Resolución si ya está vinculada; la
columna "Comisionados" concatena `persona.agente_nombreyapellido` de cada
`ComisionadoSolicitud` (Agente o Externo, vía la property `persona`).

## Firma

```python
def _solicitud_datatable_row(s: Solicitud, user) -> dict:
```

## Uso real

`datatable_solicitudes` (mismo módulo, más abajo).

## Ver también

- [Solicitud](../../../secretariador/models/Solicitud.md)
- [ComisionadoSolicitud](../../../secretariador/models/ComisionadoSolicitud.md)