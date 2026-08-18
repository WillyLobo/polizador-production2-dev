---
symbol: PaginaListaRepresentantesTecnicos
kind: function
module: carga/views/representantetecnicoviews.py
lines: 58-61
signature_hash: sha1:84735e897c2530da9a0998d80d57015181688418
authored: true
---

# PaginaListaRepresentantesTecnicos

**Módulo:** `carga/views/representantetecnicoviews.py` (líneas 58-61)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-representantetecnicos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.

## Firma

```python
def PaginaListaRepresentantesTecnicos(request):
```

## Uso real

`PaginaListaRepresentantesTecnicos` (`carga:lista-representantetecnicos`), enlazada desde el navbar/dropdown de listados.

## Ver también

- [RepresentanteTecnico](../../models/RepresentanteTecnico.md)
