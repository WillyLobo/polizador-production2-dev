---
symbol: EliminarPrograma
kind: class
module: carga/views/programaviews.py
lines: 12-17
signature_hash: sha1:26fee4ba71d4ec79b73bd3d124292e015a289df9
authored: true
---

# EliminarPrograma

**Módulo:** `carga/views/programaviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Programa, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarPrograma(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado y la ficha de Programa (botón de borrar de `polizador/context_processors.py::eliminarlinkimg`).

## Ver también

- [Programa](../../models/Programa.md)
