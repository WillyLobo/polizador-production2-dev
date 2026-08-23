---
symbol: PaginaListaEmpresas
kind: function
module: carga/views/empresaviews.py
lines: 64-67
signature_hash: sha1:866957476935207841d6963f57f44448bbf5da1e
authored: true
---

# PaginaListaEmpresas

**Módulo:** `carga/views/empresaviews.py` (líneas 64-67)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-empresas.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.

## Firma

```python
def PaginaListaEmpresas(request):
```

## Uso real

`PaginaListaEmpresas` (`carga:lista-empresas`), enlazada desde el navbar/dropdown de listados.

## Ver también

- [Empresa](../../models/Empresa.md)
