---
symbol: PaginaListaCargoTipos
kind: function
module: personalizador/views/cargotipoviews.py
lines: 52-55
signature_hash: sha1:07b5388d04bd5f684ccb696a89421c81e7bb65ac
authored: true
---

# PaginaListaCargoTipos

**Módulo:** `personalizador/views/cargotipoviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-cargotipos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaCargoTipos(request):
```

## Uso real

`PaginaListaCargoTipos` (`personalizador:lista-cargotipos`).

## Ver también

- [CargoTipo](../../models/CargoTipo.md)
