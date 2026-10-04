---
symbol: CrearPoliza
kind: class
module: carga/views/polizaviews.py
lines: 44-62
signature_hash: sha1:3e9b38ffd4f01f66f2db452ad7dc088de736e344
authored: true
---

# CrearPoliza

**Módulo:** `carga/views/polizaviews.py` (líneas 44-62) · hereda de `PermissionRequiredMixin, UserKwargsMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.CreateView`

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
