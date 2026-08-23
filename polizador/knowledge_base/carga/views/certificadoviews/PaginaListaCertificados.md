---
symbol: PaginaListaCertificados
kind: function
module: carga/views/certificadoviews.py
lines: 396-399
signature_hash: sha1:cc023534d8180ae14b9fb978a98cce3eb708df05
authored: true
---

# PaginaListaCertificados

**Módulo:** `carga/views/certificadoviews.py` (líneas 396-399)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-certificados.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.
 Nota: hay una `AjaxDatatableView` completa para Certificado comentada (deshabilitada) más abajo en `carga/views/documentosdigitalesviews.py` — código muerto, no la fuente real de datos actual.

## Firma

```python
def PaginaListaCertificados(request):
```

## Uso real

`PaginaListaCertificados` (`carga:lista-certificados`).

## Ver también

- [Certificado](../../models/Certificado.md)
