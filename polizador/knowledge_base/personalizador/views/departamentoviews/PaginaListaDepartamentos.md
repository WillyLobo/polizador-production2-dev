---
symbol: PaginaListaDepartamentos
kind: function
module: personalizador/views/departamentoviews.py
lines: 52-55
signature_hash: sha1:fba3d95035ced94c0e3b8fc648b22b393bbbd1db
authored: true
---

# PaginaListaDepartamentos

**Módulo:** `personalizador/views/departamentoviews.py` (líneas 52-55)

## Propósito

Función vista simple: solo renderiza la página que contiene la tabla (`Lista-departamentos.html`), sin
pasarle datos. La tabla se llena después vía AJAX contra un endpoint genérico de listado
(`api/views/generics.py`, fuera de `personalizador` — no cubierto en esta fase).

## Firma

```python
def PaginaListaDepartamentos(request):
```

## Uso real

`PaginaListaDepartamentos` (`personalizador:lista-departamentos`).

## Ver también

- [Departamento](../../models/Departamento.md)
