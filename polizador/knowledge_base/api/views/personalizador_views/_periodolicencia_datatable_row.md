---
symbol: _periodolicencia_datatable_row
kind: function
module: api/views/personalizador_views.py
lines: 911-932
signature_hash: sha1:7363e0fbb8e59b05f9bccb9b2a777a5b71b14d71
authored: true
---

# _periodolicencia_datatable_row

**Módulo:** `api/views/personalizador_views.py` (líneas 911-932)

## Propósito

Row-builder para `register_simple_datatable` (ver `api/views/generics.py`): arma la fila
del listado de `PeriodoLicencia`. Para `LOR_ANUAL` muestra apertura/fecha límite de
solicitud y "—" en las columnas de turno (no aplican); para `LOR_INVIERNO` es al revés,
muestra los 2 turnos combinados en texto ("`<desde>` al `<hasta>`") y "—" en
apertura/límite. `acciones` trae los links editar/eliminar solo si el usuario tiene el
permiso correspondiente (`_simple_acciones`).

`register_simple_datatable` además registra automáticamente el endpoint de detalle
(`with_detail=True` por default) que renderiza
`templates/ajax_datatable/personalizador/periodolicencia/render_row_details.html` — la
expansión de fila que lista, para el período clickeado, cada `LicenciaPermiso` vinculada
(`object.licenciapermiso_set.all`) con agente, tipo, fecha y cantidad.

## Firma

```python
def _periodolicencia_datatable_row(p: PeriodoLicencia, user) -> dict:
```

## Uso real

`register_simple_datatable(router, PeriodoLicencia, "periodolicencias", row_builder=_periodolicencia_datatable_row, ...)`.

## Ver también

- [PeriodoLicencia](../../../personalizador/models/PeriodoLicencia.md)
- [PaginaListaPeriodoLicencias](../../../personalizador/views/periodolicenciaviews/PaginaListaPeriodoLicencias.md)
