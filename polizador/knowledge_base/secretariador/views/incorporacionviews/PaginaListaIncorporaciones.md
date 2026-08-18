---
symbol: PaginaListaIncorporaciones
kind: function
module: secretariador/views/incorporacionviews.py
lines: 282-285
signature_hash: sha1:a35b3df278c2574139cc38db734ddaa752dbf9f3
authored: true
---

# PaginaListaIncorporaciones

**Módulo:** `secretariador/views/incorporacionviews.py` (líneas 282-285)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-incorporaciones.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `secretariador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaIncorporaciones(request):
```

## Uso real

`PaginaListaIncorporaciones` (`secretariador:lista-incorporaciones`).

## Ver también

- [Incorporacion](../../models/Incorporacion.md)
