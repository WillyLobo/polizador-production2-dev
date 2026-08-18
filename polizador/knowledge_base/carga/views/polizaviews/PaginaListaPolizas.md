---
symbol: PaginaListaPolizas
kind: function
module: carga/views/polizaviews.py
lines: 89-92
signature_hash: sha1:41f0b4b6871cb1fa4c4ad25256d80a841501a77b
authored: true
---

# PaginaListaPolizas

**Módulo:** `carga/views/polizaviews.py` (líneas 89-92)

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
