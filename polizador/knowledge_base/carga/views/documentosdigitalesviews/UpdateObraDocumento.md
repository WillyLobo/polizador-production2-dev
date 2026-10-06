---
symbol: UpdateObraDocumento
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 94-102
signature_hash: sha1:e0ef6b3a26eaccbbdd5f6ac12ee27f81f90fba65
authored: true
---

# UpdateObraDocumento

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 94-102) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de un `ObraDocumento` ya cargado.

Exige `carga.change_obradocumento`. Al terminar vuelve a la ficha de la Obra (`carga:estado-obra`), no a un listado.

## Firma

```python
class UpdateObraDocumento(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateObraDocumento` (`carga:update-obra-documento`).

## Ver también

- [ObraDocumento](../../models/ObraDocumento.md)
