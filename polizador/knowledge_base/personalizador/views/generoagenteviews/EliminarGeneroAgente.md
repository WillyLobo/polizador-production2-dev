---
symbol: EliminarGeneroAgente
kind: class
module: personalizador/views/generoagenteviews.py
lines: 12-17
signature_hash: sha1:6a0a8fbb8a883f52b00af96ee4a79b43c9ad2524
authored: true
---

# EliminarGeneroAgente

**Módulo:** `personalizador/views/generoagenteviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un GeneroAgente, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarGeneroAgente(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de GeneroAgente.

## Ver también

- [GeneroAgente](../../models/GeneroAgente.md)
