---
symbol: PaginaListaPolizas
kind: function
module: carga/views/polizaviews.py
lines: 167-170
signature_hash: sha1:98630e2bb9d3fe5cfc8637fdf1ad91a48150069d
authored: true
---

# PaginaListaPolizas

**Módulo:** `carga/views/polizaviews.py` (líneas 167-170)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-polizas.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.

## Firma

```python
def PaginaListaPolizas(request):
```

## Uso real

`PaginaListaPolizas` (`carga:lista-polizas`).

## Ver también

- [Poliza](../../models/Poliza.md)
