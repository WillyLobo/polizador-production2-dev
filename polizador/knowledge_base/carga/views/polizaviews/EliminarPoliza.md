---
symbol: EliminarPoliza
kind: class
module: carga/views/polizaviews.py
lines: 35-40
signature_hash: sha1:2777a7778e26010e653add381aa7d7f1b985088b
authored: true
---

# EliminarPoliza

**Módulo:** `carga/views/polizaviews.py` (líneas 35-40) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Poliza, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarPoliza(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Póliza.

## Ver también

- [Poliza](../../models/Poliza.md)
