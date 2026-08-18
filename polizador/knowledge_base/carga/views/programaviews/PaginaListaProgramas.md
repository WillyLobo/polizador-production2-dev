---
symbol: PaginaListaProgramas
kind: function
module: carga/views/programaviews.py
lines: 58-61
signature_hash: sha1:2e076ea770a0e3cfb852b3a9f0b08f51a1ec115d
authored: true
---

# PaginaListaProgramas

**Módulo:** `carga/views/programaviews.py` (líneas 58-61)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-programas.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.

## Firma

```python
def PaginaListaProgramas(request):
```

## Uso real

`PaginaListaProgramas` (`carga:lista-programas`), enlazada desde el navbar/dropdown de listados.

## Ver también

- [Programa](../../models/Programa.md)
