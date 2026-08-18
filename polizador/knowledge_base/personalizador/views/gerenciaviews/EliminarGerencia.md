---
symbol: EliminarGerencia
kind: class
module: personalizador/views/gerenciaviews.py
lines: 12-17
signature_hash: sha1:c472498854353badcbda3039ae6f0da648ef28ef
authored: true
---

# EliminarGerencia

**Módulo:** `personalizador/views/gerenciaviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Gerencia, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarGerencia(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Gerencia.

## Ver también

- [Gerencia](../../models/Gerencia.md)
