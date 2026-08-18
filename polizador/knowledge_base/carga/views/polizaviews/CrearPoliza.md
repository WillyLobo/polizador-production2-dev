---
symbol: CrearPoliza
kind: class
module: carga/views/polizaviews.py
lines: 22-40
signature_hash: sha1:abad3099aa9336c6745088025e3c2f46ef27bfbb
authored: true
---

# CrearPoliza

**Módulo:** `carga/views/polizaviews.py` (líneas 22-40) · hereda de `PermissionRequiredMixin, UserKwargsMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.CreateView`

## Propósito

Alta de Póliza junto con su formset inline de `Poliza_Movimiento` (el primer movimiento) — usa `UserKwargsMixin`/`UserFormsetKwargsMixin` para que el form/formset tengan acceso al usuario logueado (probablemente para defaults o filtros por permiso, ver `core/mixins.py`).

## Firma

```python
class CrearPoliza(PermissionRequiredMixin, UserKwargsMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.CreateView):
```

## Uso real

`CrearPoliza` (`carga:crear-poliza`), enlazada desde la ficha de Obra.

## Ver también

- [Poliza](../../models/Poliza.md)
- [Poliza_Movimiento](../../models/Poliza_Movimiento.md)
