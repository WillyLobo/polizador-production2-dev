---
symbol: PaginaListaRegiones
kind: function
module: carga/views/regionviews.py
lines: 58-61
signature_hash: sha1:079a56a1c66ab073913653b66aa77be5ec6fb571
authored: true
---

# PaginaListaRegiones

**Módulo:** `carga/views/regionviews.py` (líneas 58-61)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-regions.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.

## Firma

```python
def PaginaListaRegiones(request):
```

## Uso real

`PaginaListaRegiones` (`carga:lista-regions`), enlazada desde el navbar/dropdown de listados.

## Ver también

- [Region](../../models/Region.md)
