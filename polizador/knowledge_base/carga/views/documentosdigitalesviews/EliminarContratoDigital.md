---
symbol: EliminarContratoDigital
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 56-63
signature_hash: sha1:296132719857b3e0052aab7d38c791ba1e78bb69
authored: true
---

# EliminarContratoDigital

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 56-63) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un ContratosDigitales, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

Exige el permiso propio del modelo (`carga.delete_contratosdigitales`; antes pedía por error el de `certificado`). Al terminar vuelve a la ficha de la Obra del Contrato (`carga:estado-obra`), no a un listado.

## Firma

```python
class EliminarContratoDigital(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde la ficha de Obra/Contrato.

## Ver también

- [ContratosDigitales](../../models/ContratosDigitales.md)
