---
symbol: PaginaListaObras
kind: function
module: carga/views/obraviews.py
lines: 166-176
signature_hash: sha1:768cd9aa8ca5149c7da874d037df3333ecadc37c
authored: true
---

# PaginaListaObras

**Módulo:** `carga/views/obraviews.py` (líneas 166-176)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-obras.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.

## Firma

```python
def PaginaListaObras(request):
```

## Uso real

`PaginaListaObras` (`carga:lista-obras`) — destino por defecto tras crear/borrar una Obra.

## Ver también

- [Obra](../../models/Obra.md)
