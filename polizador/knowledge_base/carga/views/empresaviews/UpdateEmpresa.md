---
symbol: UpdateEmpresa
kind: class
module: carga/views/empresaviews.py
lines: 42-48
signature_hash: sha1:c5e6041246c8c98ec907573230db82331afd7d68
authored: true
---

# UpdateEmpresa

**Módulo:** `carga/views/empresaviews.py` (líneas 42-48) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Empresa vía `ModelForm` estándar.

## Firma

```python
class UpdateEmpresa(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateEmpresa` (`carga:update-empresa`), enlazada desde el listado/ficha.

## Ver también

- [Empresa](../../models/Empresa.md)
