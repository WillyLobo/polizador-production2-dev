---
symbol: PaginaListaDirectorios
kind: function
module: personalizador/views/directorioviews.py
lines: 52-55
signature_hash: sha1:2d7f86ae391c266717cc35a6c2cbea5637157fe4
authored: true
---

# PaginaListaDirectorios

**Módulo:** `personalizador/views/directorioviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-directorios.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaDirectorios(request):
```

## Uso real

`PaginaListaDirectorios` (`personalizador:lista-directorios`).

## Ver también

- [Directorio](../../models/Directorio.md)
