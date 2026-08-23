---
symbol: PaginaListaDepartamentos
kind: function
module: carga/views/departamentoviews.py
lines: 57-60
signature_hash: sha1:dd047b9c7f38425440a106806261e521d0cf8d0f
authored: true
---

# PaginaListaDepartamentos

**Módulo:** `carga/views/departamentoviews.py` (líneas 57-60)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-departamentos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `carga` — no cubierto en esta fase), siguiendo el
patrón `django-ajax-datatable` que describe CLAUDE.md.

## Firma

```python
def PaginaListaDepartamentos(request):
```

## Uso real

`PaginaListaDepartamentos` (`carga:lista-departamentos`), enlazada desde el navbar/dropdown de listados.

## Ver también

- [Departamento](../../models/Departamento.md)
