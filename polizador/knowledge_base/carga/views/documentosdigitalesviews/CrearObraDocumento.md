---
symbol: CrearObraDocumento
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 66-91
signature_hash: sha1:94a3d667d2e8b4616f8f29786c523ffe840e2ca6
authored: true
---

# CrearObraDocumento

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 66-91) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un documento PDF adjunto a una Obra (`ObraDocumento`). Si viene `?obra=<id>`, precarga la Obra destino.

Exige `carga.add_obradocumento`. Al terminar vuelve a la ficha de la Obra (`carga:estado-obra`), no a un listado.

## Firma

```python
class CrearObraDocumento(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearObraDocumento` (`carga:crear-obra-documento`), enlazada desde la ficha de Obra.

## Ver también

- [ObraDocumento](../../models/ObraDocumento.md)
