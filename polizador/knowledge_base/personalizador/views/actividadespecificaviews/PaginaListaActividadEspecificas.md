---
symbol: PaginaListaActividadEspecificas
kind: function
module: personalizador/views/actividadespecificaviews.py
lines: 52-55
signature_hash: sha1:2a161c7a47b0f2e094a65d9c2e36dd338f2495e4
authored: true
---

# PaginaListaActividadEspecificas

**Módulo:** `personalizador/views/actividadespecificaviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-actividadespecificas.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaActividadEspecificas(request):
```

## Uso real

`PaginaListaActividadEspecificas` (`personalizador:lista-actividadespecificas`).

## Ver también

- [ActividadEspecifica](../../models/ActividadEspecifica.md)
