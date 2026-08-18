---
symbol: EliminarAgente
kind: class
module: personalizador/views/agenteviews.py
lines: 14-19
signature_hash: sha1:0e4f84b3d0a88af9811ca900007556c7321a4863
authored: true
---

# EliminarAgente

**Módulo:** `personalizador/views/agenteviews.py` (líneas 14-19) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Agente, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarAgente(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Agente.

## Ver también

- [Agente](../../models/Agente.md)
