---
symbol: register_simple_datatable
kind: function
module: api/views/generics.py
lines: 102-181
signature_hash: sha1:cf91db5e722fda45bd3c744bcb71a4c2c339324b
authored: true
---

# register_simple_datatable

**Módulo:** `api/views/generics.py` (líneas 102-181)

## Propósito

La pieza central de infraestructura de todo `api/views/*.py`: registra el par de
endpoints `GET /datatables/<url_slug>/` (+ `.../<id>/detalle/` salvo `with_detail=False`)
para un listado "simple" — un modelo, un puñado de columnas, links de acción gateados por
permiso, sin cómputo bespoke por fila más allá de `row_builder(obj, user) -> dict`. Según
su propio docstring, reemplaza ~10 listados tipo catálogo (Aseguradora, Programa,
Departamento...) que antes eran copias casi idénticas del mismo boilerplate de
`AjaxDatatableView`.

`boolean_filter_keys` es el mecanismo para que un filtro de `<select>` sobre un
`BooleanField` funcione: sin esto, el string `"true"`/`"false"` que manda el frontend se
pasaría tal cual a `.filter(campo="true")`, que nunca matchea un booleano real — con la
clave listada acá, se coerciona a `bool` antes de filtrar (mismo patrón que
`datatable_solicitudes`/`datatable_obras` hacen a mano para sus propios filtros
booleanos, fuera de este helper).

No es un símbolo capturado en el manifest — se generan dos funciones internas (`_list`,
`_detalle`) que quedan registradas en el router, sin nombre propio expuesto al resto del
código; por eso cada `register_simple_datatable(...)` de `carga_views.py`/
`personalizador_views.py`/`secretariador_views.py` es una *llamada*, no una función
nombrada, y no tiene su propia página en esta base de conocimiento — se documenta acá,
en su definición.

## Firma

```python
def register_simple_datatable(router, model, url_slug: str, *, order_fields: dict, filter_fields: dict, search_lookups: list, row_builder, default_order: str='id', queryset=None, with_detail: bool=True, boolean_filter_keys: frozenset=frozenset()):
```

## Uso real

Todos los `register_simple_datatable(router, Modelo, "slug", ...)` de `carga_views.py`, `personalizador_views.py`, `secretariador_views.py`.

## Ver también

- [PerPagePagination](PerPagePagination.md)
- [parse_order_by](parse_order_by.md)
- [render_datatable_row_details](render_datatable_row_details.md)
