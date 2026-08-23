---
symbol: datatable_solicitudes
kind: function
module: api/views/secretariador_views.py
lines: 694-762
signature_hash: sha1:28a4335391f20c931ff37afbbe28c279873712d7
authored: true
---

# datatable_solicitudes

**Módulo:** `api/views/secretariador_views.py` (líneas 694-762)

## Propósito

El listado principal de Solicitudes: filtros a mano (no `register_simple_datatable`) con
un caso especial — el filtro "Comisionados" busca tanto en `comisionadosolicitud_nombre`
(Agente) como en `comisionadosolicitud_externo` (Externo) con un `Q` OR, porque son dos
FKs mutuamente excluyentes del mismo concepto lógico. `solicitud_dia_inhabil` es un
filtro booleano (coerción manual de `"true"/"1"` string a bool, mismo patrón que
`register_simple_datatable`'s `boolean_filter_keys` mecaniza para el caso genérico).

## Firma

```python
def datatable_solicitudes(request, draw: int=1, start: int=0, length: int=50, search: str='', order_by: str='-solicitud_actuacion_ano,-solicitud_actuacion_numero', filters: str='{}'):
```

## Uso real

`GET /v1/api/datatables/solicitudes/` — consumido por `Lista-solicitudes.html`.

## Ver también

- [Solicitud](../../../secretariador/models/Solicitud.md)
- [_solicitud_datatable_row](_solicitud_datatable_row.md)
