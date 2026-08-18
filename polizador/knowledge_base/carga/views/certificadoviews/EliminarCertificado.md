---
symbol: EliminarCertificado
kind: class
module: carga/views/certificadoviews.py
lines: 183-188
signature_hash: sha1:0324e7ec8b37b081d562921c9b9f4d2416e27757
authored: true
---

# EliminarCertificado

**Módulo:** `carga/views/certificadoviews.py` (líneas 183-188) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

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
