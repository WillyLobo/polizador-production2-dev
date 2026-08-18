---
symbol: PaginaListaAseguradoras
kind: function
module: carga/views/aseguradoraviews.py
lines: 52-55
signature_hash: sha1:e0fd7e88bed3af98ce7ad644e3ee3adbe8ba5a35
authored: true
---

# PaginaListaAseguradoras

**Módulo:** `carga/views/aseguradoraviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-aseguradoras.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.

## Firma

```python
def PaginaListaAseguradoras(request):
```

## Uso real

`PaginaListaAseguradoras` (`carga:lista-aseguradoras`), enlazada desde el navbar/dropdown de listados.

## Ver también

- [Aseguradora](../../models/Aseguradora.md)
