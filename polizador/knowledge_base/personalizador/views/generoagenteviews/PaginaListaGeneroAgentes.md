---
symbol: PaginaListaGeneroAgentes
kind: function
module: personalizador/views/generoagenteviews.py
lines: 52-55
signature_hash: sha1:418c3561ec97d3eafdc0123fb7848f9ccf69564d
authored: true
---

# PaginaListaGeneroAgentes

**Módulo:** `personalizador/views/generoagenteviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-generoagentes.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaGeneroAgentes(request):
```

## Uso real

`PaginaListaGeneroAgentes` (`personalizador:lista-generoagentes`).

## Ver también

- [GeneroAgente](../../models/GeneroAgente.md)
