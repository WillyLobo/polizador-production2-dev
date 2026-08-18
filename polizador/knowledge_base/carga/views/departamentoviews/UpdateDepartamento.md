---
symbol: UpdateDepartamento
kind: class
module: carga/views/departamentoviews.py
lines: 41-47
signature_hash: sha1:87467e66eb456f2d27b7b3f6492f5b1f1ab62508
authored: true
---

# UpdateDepartamento

**Módulo:** `carga/views/departamentoviews.py` (líneas 41-47) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Departamento vía `ModelForm` estándar.

## Firma

```python
class UpdateDepartamento(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateDepartamento` (`carga:update-departamento`), enlazada desde el listado/ficha.

## Ver también

- [Departamento](../../models/Departamento.md)
