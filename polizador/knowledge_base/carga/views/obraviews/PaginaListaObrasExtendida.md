---
symbol: PaginaListaObrasExtendida
kind: function
module: carga/views/obraviews.py
lines: 179-182
signature_hash: sha1:6328f6619ffa1e9b1c43b5c0f5c62376c995d379
authored: true
---

# PaginaListaObrasExtendida

**Módulo:** `carga/views/obraviews.py` (líneas 179-182)

## Propósito

Variante de `PaginaListaObras` con más columnas/filtros ("extendida") — mismo patrón de página vacía + tabla AJAX, sin `permission_required` explícito propio (solo `login_required`).

## Firma

```python
def PaginaListaObrasExtendida(request):
```

## Uso real

`PaginaListaObrasExtendida` (`carga:lista-obras-extendida`).

## Ver también

- [PaginaListaObras](PaginaListaObras.md)
