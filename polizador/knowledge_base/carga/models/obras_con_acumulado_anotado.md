---
symbol: obras_con_acumulado_anotado
kind: function
module: carga/models.py
lines: 546-558
signature_hash: sha1:6cf6bfc962f51195118d72edababba887d65d071
authored: true
---

# obras_con_acumulado_anotado

**Módulo:** `carga/models.py` (líneas 546-558)

## Propósito

Anota en una sola query (vía `Subquery`) el % acumulado del último Certificado de avance y
el % acumulado de Anticipo del último Certificado de Anticipo de cada Obra del queryset —
pensada para listados de Obras que necesitan mostrar esos dos números sin un N+1 (una
query de Certificado por Obra listada).

**Corrección sobre una nota anterior de esta misma página:** está importada en
`carga/views/obraviews.py` pero ningún lugar de ese archivo la llama (`grep` solo
encuentra el import, no una call-site) — eso llevó a documentar acá, en una pasada
anterior, que parecía código muerto. No lo es: sí se usa, pero desde `api`, no desde
`carga`. `api/views/carga_views.py::datatable_obras` es la call-site real — el endpoint
detrás del listado principal de Obras (`Lista-obras.html`) la llama para poder mostrar
las columnas de % acumulado sin un N+1 (una query de Certificado por Obra listada). El
import muerto en `obraviews.py` sigue siendo genuinamente muerto y podría limpiarse, pero
la función en sí está viva.

## Firma

```python
def obras_con_acumulado_anotado(queryset):
```

## Uso real

`api/views/carga_views.py::datatable_obras` — `obras_con_acumulado_anotado(queryset)`
sobre el queryset de Obras antes de paginar/serializar; `_obra_datatable_row` lee las dos
columnas anotadas (`obra_acum_pct_anotado`/`obra_anticipo_acumulado_anotado`) vía
`getattr(o, ..., None)`, asumiendo que quien armó el queryset ya corrió esta función.

## Ver también

- [Obra](Obra.md)
- [Certificado](Certificado.md)
- [datatable_obras](../../api/views/carga_views/datatable_obras.md)
- [_obra_datatable_row](../../api/views/carga_views/_obra_datatable_row.md)
