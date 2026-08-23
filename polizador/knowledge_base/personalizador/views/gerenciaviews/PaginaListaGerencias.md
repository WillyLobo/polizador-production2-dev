---
symbol: PaginaListaGerencias
kind: function
module: personalizador/views/gerenciaviews.py
lines: 52-55
signature_hash: sha1:7fb90decff558a7f2df52c66c77baf724e3ba88f
authored: true
---

# PaginaListaGerencias

**Módulo:** `personalizador/views/gerenciaviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-gerencias.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaGerencias(request):
```

## Uso real

`PaginaListaGerencias` (`personalizador:lista-gerencias`).

## Ver también

- [Gerencia](../../models/Gerencia.md)
