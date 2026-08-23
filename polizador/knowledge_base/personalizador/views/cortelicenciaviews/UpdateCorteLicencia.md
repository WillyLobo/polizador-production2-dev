---
symbol: UpdateCorteLicencia
kind: class
module: personalizador/views/cortelicenciaviews.py
lines: 43-57
signature_hash: sha1:b4ed74b61b38317bd60481b4c5ef19a89c6d2ee7
authored: true
---

# UpdateCorteLicencia

**Módulo:** `personalizador/views/cortelicenciaviews.py` (líneas 43-57) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de un Corte de Licencia. `get_success_url` (no fijo) vuelve siempre a la ficha de la LicenciaPermiso interrumpida, no a un listado de cortes (no existe tal listado — un corte solo se ve/edita desde la licencia a la que pertenece).

## Firma

```python
class UpdateCorteLicencia(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateCorteLicencia` (`personalizador:update-cortelicencia`).

## Ver también

- [CorteLicencia](../../models/CorteLicencia.md)
