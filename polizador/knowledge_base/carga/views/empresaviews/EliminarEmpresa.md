---
symbol: EliminarEmpresa
kind: class
module: carga/views/empresaviews.py
lines: 12-17
signature_hash: sha1:8194fc1d9c1aac90833e0cc7e7d84ac6cdc34aa1
authored: true
---

# EliminarEmpresa

**Módulo:** `carga/views/empresaviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Empresa, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarEmpresa(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado y la ficha de Empresa (botón de borrar de `polizador/context_processors.py::eliminarlinkimg`).

## Ver también

- [Empresa](../../models/Empresa.md)
