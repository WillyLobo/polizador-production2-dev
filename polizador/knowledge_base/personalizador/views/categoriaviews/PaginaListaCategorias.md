---
symbol: PaginaListaCategorias
kind: function
module: personalizador/views/categoriaviews.py
lines: 52-55
signature_hash: sha1:d5624e5e29d21a14104d29e58f8b5c5fc602f549
authored: true
---

# PaginaListaCategorias

**Módulo:** `personalizador/views/categoriaviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-categorias.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaCategorias(request):
```

## Uso real

`PaginaListaCategorias` (`personalizador:lista-categorias`).

## Ver también

- [Categoria](../../models/Categoria.md)
