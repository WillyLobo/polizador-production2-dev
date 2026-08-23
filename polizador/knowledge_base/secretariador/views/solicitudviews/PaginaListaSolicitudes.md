---
symbol: PaginaListaSolicitudes
kind: function
module: secretariador/views/solicitudviews.py
lines: 200-203
signature_hash: sha1:c6563bc9b6ee56bacfd7e6a5ef3c7904ab557895
authored: true
---

# PaginaListaSolicitudes

**Módulo:** `secretariador/views/solicitudviews.py` (líneas 200-203)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-solicitudes.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `secretariador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaSolicitudes(request):
```

## Uso real

`PaginaListaSolicitudes` (`secretariador:lista-solicitudes`).

## Ver también

- [Solicitud](../../models/Solicitud.md)
