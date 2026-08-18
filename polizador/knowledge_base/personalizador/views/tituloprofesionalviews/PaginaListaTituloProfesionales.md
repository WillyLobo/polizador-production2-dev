---
symbol: PaginaListaTituloProfesionales
kind: function
module: personalizador/views/tituloprofesionalviews.py
lines: 52-55
signature_hash: sha1:95e128807b48b2868f8a5b6c11b951ae0ab35f1b
authored: true
---

# PaginaListaTituloProfesionales

**Módulo:** `personalizador/views/tituloprofesionalviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-tituloprofesionales.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaTituloProfesionales(request):
```

## Uso real

`PaginaListaTituloProfesionales` (`personalizador:lista-tituloprofesionales`).

## Ver también

- [TituloProfesional](../../models/TituloProfesional.md)
