---
symbol: UpdateRepresentanteTecnico
kind: class
module: carga/views/representantetecnicoviews.py
lines: 41-47
signature_hash: sha1:5fe07cb866e9e33386519aba2578f55ea8ded30d
authored: true
---

# UpdateRepresentanteTecnico

**Módulo:** `carga/views/representantetecnicoviews.py` (líneas 41-47) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de RepresentanteTecnico vía `ModelForm` estándar.

## Firma

```python
class UpdateRepresentanteTecnico(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateRepresentanteTecnico` (`carga:update-representantetecnico`), enlazada desde el listado/ficha.

## Ver también

- [RepresentanteTecnico](../../models/RepresentanteTecnico.md)
