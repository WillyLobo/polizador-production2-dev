---
symbol: UpdateMunicipio
kind: class
module: carga/views/municipioviews.py
lines: 41-47
signature_hash: sha1:e7556f8ab6f45219ab574dcf8e8938ee8d763e49
authored: true
---

# UpdateMunicipio

**Módulo:** `carga/views/municipioviews.py` (líneas 41-47) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Municipio vía `ModelForm` estándar.

## Firma

```python
class UpdateMunicipio(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateMunicipio` (`carga:update-municipio`), enlazada desde el listado/ficha.

## Ver también

- [Municipio](../../models/Municipio.md)
