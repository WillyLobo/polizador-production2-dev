---
symbol: PaginaListaAgentes
kind: function
module: personalizador/views/agenteviews.py
lines: 86-89
signature_hash: sha1:7558eacc471f8a44d437fc419d4d9a4598dc64aa
authored: true
---

# PaginaListaAgentes

**Módulo:** `personalizador/views/agenteviews.py` (líneas 86-89)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-agentes.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaAgentes(request):
```

## Uso real

`PaginaListaAgentes` (`personalizador:lista-agentes`).

## Ver también

- [Agente](../../models/Agente.md)
