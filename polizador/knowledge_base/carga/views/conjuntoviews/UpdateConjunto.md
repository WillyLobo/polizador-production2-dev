---
symbol: UpdateConjunto
kind: class
module: carga/views/conjuntoviews.py
lines: 40-46
signature_hash: sha1:84dfdd06c78fa286eaffcb07823f4466826605fd
authored: true
---

# UpdateConjunto

**Módulo:** `carga/views/conjuntoviews.py` (líneas 40-46) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de ConjuntoLicitado vía `ModelForm` estándar.

## Firma

```python
class UpdateConjunto(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateConjunto` (`carga:update-conjunto`), enlazada desde el listado/ficha.

## Ver también

- [ConjuntoLicitado](../../models/ConjuntoLicitado.md)
