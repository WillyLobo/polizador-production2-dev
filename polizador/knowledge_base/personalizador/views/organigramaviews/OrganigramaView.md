---
symbol: OrganigramaView
kind: function
module: personalizador/views/organigramaviews.py
lines: 151-156
signature_hash: sha1:2e74ec727acb024d7a089b80691cdfbd537ef2d0
authored: true
---

# OrganigramaView

**Módulo:** `personalizador/views/organigramaviews.py` (líneas 151-156)

## Propósito

Vista de función que sirve la página del organigrama institucional. Requiere login y el
permiso `personalizador.view_directorio` (`raise_exception=True`, así un usuario sin
permiso recibe 403 en vez de un redirect a login).

## Firma

```python
def OrganigramaView(request):
```

## Uso real

Registrada en `personalizador/urls.py` como `path("organigrama/", OrganigramaView,
name="organigrama")`. Sin candidatos de uso interno detectados por grep — es un endpoint,
no una función reusada.

## Flujo de datos

Delega el armado del diagrama a `_build_organigrama_mermaid()`, que devuelve
`(mermaid_source, counts)`, y los pasa tal cual al contexto del template
`organigrama.html` (presumiblemente renderizado del lado del cliente con mermaid.js).

## Ver también

- [_build_organigrama_mermaid](../organigramaviews/_build_organigrama_mermaid.md) — arma el diagrama que esta vista sirve.
