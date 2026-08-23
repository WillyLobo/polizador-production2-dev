---
symbol: PaginaListaConjuntos
kind: function
module: carga/views/conjuntoviews.py
lines: 57-60
signature_hash: sha1:d852cc5f23e288977a4146cafa2004fea3c7accc
authored: true
---

# PaginaListaConjuntos

**Módulo:** `carga/views/conjuntoviews.py` (líneas 57-60)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-conjuntos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.

## Firma

```python
def PaginaListaConjuntos(request):
```

## Uso real

`PaginaListaConjuntos` (`carga:lista-conjuntos`), enlazada desde el navbar/dropdown de listados.

## Ver también

- [ConjuntoLicitado](../../models/ConjuntoLicitado.md)
