---
symbol: PaginaListaCertificados
kind: function
module: carga/views/certificadoviews.py
lines: 229-232
signature_hash: sha1:c317d8fc0ea479342722f8084aaf0d5e31481066
authored: true
---

# PaginaListaCertificados

**Módulo:** `carga/views/certificadoviews.py` (líneas 229-232)

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
