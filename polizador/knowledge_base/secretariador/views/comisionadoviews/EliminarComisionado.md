---
symbol: EliminarComisionado
kind: class
module: secretariador/views/comisionadoviews.py
lines: 41-46
signature_hash: sha1:fa4a9099733a69e52404e025cab261d0fe1eb928
authored: true
---

# EliminarComisionado

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 41-46) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Agente (comisionado), mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarComisionado(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado de comisionados.

## Ver también

- [Agente](../../../personalizador/models/Agente.md)
