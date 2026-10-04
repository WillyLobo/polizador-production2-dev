---
symbol: EliminarCertificado
kind: class
module: carga/views/certificadoviews.py
lines: 26-31
signature_hash: sha1:bd66ad5075f9b3a60b696845706d9a26ec6f4eed
authored: true
---

# EliminarCertificado

**Módulo:** `carga/views/certificadoviews.py` (líneas 26-31) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Certificado, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarCertificado(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Certificado.

## Ver también

- [Certificado](../../models/Certificado.md)
