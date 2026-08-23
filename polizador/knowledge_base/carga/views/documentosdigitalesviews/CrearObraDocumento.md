---
symbol: CrearObraDocumento
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 60-83
signature_hash: sha1:20f3c69a86e1b12917c43ed5d722eae1b2ecbeee
authored: true
---

# CrearObraDocumento

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 60-83) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un documento PDF adjunto a una Obra (`ObraDocumento`). Si viene `?obra=<id>`, precarga la Obra destino.

## Firma

```python
class CrearObraDocumento(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearObraDocumento` (`carga:crear-obra-documento`), enlazada desde la ficha de Obra.

## Ver también

- [ObraDocumento](../../models/ObraDocumento.md)
