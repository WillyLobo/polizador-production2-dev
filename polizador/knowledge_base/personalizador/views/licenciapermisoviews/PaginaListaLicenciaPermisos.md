---
symbol: PaginaListaLicenciaPermisos
kind: function
module: personalizador/views/licenciapermisoviews.py
lines: 91-94
signature_hash: sha1:567b4185b172ebd17c20f8a9ee7443489f19586c
authored: true
---

# PaginaListaLicenciaPermisos

**Módulo:** `personalizador/views/licenciapermisoviews.py` (líneas 91-94)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-licenciapermisos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaLicenciaPermisos(request):
```

## Uso real

`PaginaListaLicenciaPermisos` (`personalizador:lista-licenciapermisos`).

## Ver también

- [LicenciaPermiso](../../models/LicenciaPermiso.md)
