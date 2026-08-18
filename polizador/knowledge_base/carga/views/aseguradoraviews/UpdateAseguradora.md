---
symbol: UpdateAseguradora
kind: class
module: carga/views/aseguradoraviews.py
lines: 42-48
signature_hash: sha1:ff89fdc962c4a266ff46d4642c137165688a42b2
authored: true
---

# UpdateAseguradora

**Módulo:** `carga/views/aseguradoraviews.py` (líneas 42-48) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Aseguradora vía `ModelForm` estándar.

## Firma

```python
class UpdateAseguradora(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateAseguradora` (`carga:update-aseguradora`), enlazada desde el listado/ficha.

## Ver también

- [Aseguradora](../../models/Aseguradora.md)
