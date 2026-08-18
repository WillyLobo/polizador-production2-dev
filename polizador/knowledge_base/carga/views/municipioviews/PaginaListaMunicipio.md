---
symbol: PaginaListaMunicipio
kind: function
module: carga/views/municipioviews.py
lines: 58-61
signature_hash: sha1:933e866ce3990c3e5b9a05f3f7581aa9380b5bb0
authored: true
---

# PaginaListaMunicipio

**Módulo:** `carga/views/municipioviews.py` (líneas 58-61)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-municipios.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.

## Firma

```python
def PaginaListaMunicipio(request):
```

## Uso real

`PaginaListaMunicipio` (`carga:lista-municipios`), enlazada desde el navbar/dropdown de listados.

## Ver también

- [Municipio](../../models/Municipio.md)
