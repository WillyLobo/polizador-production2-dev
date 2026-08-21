---
symbol: EliminarPeriodoLicencia
kind: class
module: personalizador/views/periodolicenciaviews.py
lines: 12-17
signature_hash: sha1:589ef90e40c19251e8d70028ca310ea5832149f3
authored: true
---

# EliminarPeriodoLicencia

**Módulo:** `personalizador/views/periodolicenciaviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un `PeriodoLicencia`, mostrando antes (vía
`DeleteRelatedObjectsMixin` — `core/mixins.py` + `core/deletion.py::get_deleted_objects`)
los objetos relacionados que se borrarían en cascada. En la práctica esto importa: como
`LicenciaPermiso.licenciapermiso_periodo` usa `on_delete=PROTECT`, un período con
licencias ya cargadas no se puede borrar — solo llega a confirmarse el borrado de
períodos sin uso (ej. uno creado por error).

## Firma

```python
class EliminarPeriodoLicencia(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde `Lista-periodolicencias.html`.

## Ver también

- [PeriodoLicencia](../../models/PeriodoLicencia.md)
