---
symbol: PaginaListaTipoLicenciaPermisos
kind: function
module: personalizador/views/tipolicenciapermisoviews.py
lines: 52-55
signature_hash: sha1:8cb632387777da101dd0f2e8ed56912131c12566
authored: true
---

# PaginaListaTipoLicenciaPermisos

**Módulo:** `personalizador/views/tipolicenciapermisoviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-tipolicenciapermisos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaTipoLicenciaPermisos(request):
```

## Uso real

`PaginaListaTipoLicenciaPermisos` (`personalizador:lista-tipolicenciapermisos`).

## Ver también

- [TipoLicenciaPermiso](../../models/TipoLicenciaPermiso.md)
