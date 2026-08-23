---
symbol: EliminarAseguradora
kind: class
module: carga/views/aseguradoraviews.py
lines: 12-17
signature_hash: sha1:f4568302985fc5f31a0ef0d51f288562332c868c
authored: true
---

# EliminarAseguradora

**Módulo:** `carga/views/aseguradoraviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Aseguradora, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarAseguradora(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado y la ficha de Aseguradora (botón de borrar de `polizador/context_processors.py::eliminarlinkimg`).

## Ver también

- [Aseguradora](../../models/Aseguradora.md)
