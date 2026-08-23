---
symbol: PaginaListaGrupoCargos
kind: function
module: personalizador/views/grupocargoviews.py
lines: 52-55
signature_hash: sha1:bf1cdec2090e8f2fee5fc17b6a35f4c5328bb780
authored: true
---

# PaginaListaGrupoCargos

**Módulo:** `personalizador/views/grupocargoviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-grupocargos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaGrupoCargos(request):
```

## Uso real

`PaginaListaGrupoCargos` (`personalizador:lista-grupocargos`).

## Ver también

- [GrupoCargo](../../models/GrupoCargo.md)
