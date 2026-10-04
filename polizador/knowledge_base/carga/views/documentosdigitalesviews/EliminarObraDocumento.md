---
symbol: EliminarObraDocumento
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 105-112
signature_hash: sha1:c2e6c97833580cf4d73ea6ac6057193f742923b4
authored: true
---

# EliminarObraDocumento

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 105-112) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un ObraDocumento, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

Exige `carga.delete_obradocumento`. Al terminar vuelve a la ficha de la Obra (`carga:estado-obra`), no a un listado.

## Firma

```python
class EliminarObraDocumento(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde la ficha de Obra.

## Ver también

- [ObraDocumento](../../models/ObraDocumento.md)
