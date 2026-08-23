---
symbol: datatable_obras
kind: function
module: api/views/carga_views.py
lines: 867-916
signature_hash: sha1:87e094cceeca829e7af1ab6750b69770a74d5b8f
authored: true
---

# datatable_obras

**Módulo:** `api/views/carga_views.py` (líneas 867-916)

## Propósito

El endpoint real detrás del listado principal de Obras (reemplaza al `AjaxDatatableView` comentado que quedó muerto en `carga/views/documentosdigitalesviews.py`): pagina/filtra/busca a mano (no usa `register_simple_datatable` porque necesita `obras_con_acumulado_anotado()` para las dos columnas de % acumulado, algo que el helper genérico no contempla) sobre un queryset con `select_related`+`prefetch_related` completo.

## Firma

```python
def datatable_obras(request, draw: int=1, start: int=0, length: int=50, search: str='', order_by: str='-id', filters: str='{}'):
```

## Uso real

`GET /v1/api/datatables/obras/` — consumido por `Lista-obras.html` (`carga:lista-obras`).

## Ver también

- [Obra](../../../carga/models/Obra.md)
- [_obra_datatable_row](_obra_datatable_row.md)
- [obras_con_acumulado_anotado](../../../carga/models/obras_con_acumulado_anotado.md)
