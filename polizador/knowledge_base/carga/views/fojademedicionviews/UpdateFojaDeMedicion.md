---
symbol: UpdateFojaDeMedicion
kind: class
module: carga/views/fojademedicionviews.py
lines: 190-248
signature_hash: sha1:1c212e731de2b6302e0b7f64f1fc7e43d95a17c0
authored: true
---

# UpdateFojaDeMedicion

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 190-248) · hereda de `PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView`

## Propósito

Mismo patrón `get`/`post` manual que `CrearFojaDeMedicion` (formset de items + formset de fotos), sin la parte de precarga por querystring ni de vinculación legacy (una Foja ya creada ya tiene su rubro fijo). `prepare_formset` repuebla el `%` anterior de cada fila al reconstruir el formset, tanto al mostrarlo (`get`) como al re-renderizarlo con errores (`post`).

## Firma

```python
class UpdateFojaDeMedicion(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
```

## Uso real

Ver [recalcular_acumulado_fojas_siguientes § Uso real](../../signals/recalcular_acumulado_fojas_siguientes.md#uso-real) — es la vista citada ahí (`carga/views/fojademedicionviews.py:232`).

## Ver también

- [FojaDeMedicion](../../models/FojaDeMedicion.md)
- [CrearFojaDeMedicion](CrearFojaDeMedicion.md)
