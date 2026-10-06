---
symbol: UpdateFojaDeMedicion
kind: class
module: carga/views/fojademedicionviews.py
lines: 194-253
signature_hash: sha1:a510fbd935028348f2f20480df32e7d800d69333
authored: true
---

# UpdateFojaDeMedicion

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 194-253) · hereda de `LogInvalidFormMixin, PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView`

## Propósito

Mismo patrón `get`/`post` manual que `CrearFojaDeMedicion` (formset de items + formset de fotos), sin la parte de precarga por querystring ni de vinculación legacy (una Foja ya creada ya tiene su rubro fijo). `prepare_formset` repuebla el `%` anterior de cada fila al reconstruir el formset, tanto al mostrarlo (`get`) como al re-renderizarlo con errores (`post`).

Igual que `CrearFojaDeMedicion`, su `post()` es totalmente custom y por eso invoca
`self._log_form_debug(form, formset, foto_formset)` a mano en el branch inválido — el
hook automático de `LogInvalidFormMixin` no se dispara en ninguna de las dos vistas.

## Firma

```python
class UpdateFojaDeMedicion(LogInvalidFormMixin, PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
```

## Uso real

Ver [recalcular_acumulado_fojas_siguientes § Uso real](../../signals/recalcular_acumulado_fojas_siguientes.md#uso-real) — es la vista citada ahí (`carga/views/fojademedicionviews.py:232`).

## Ver también

- [FojaDeMedicion](../../models/FojaDeMedicion.md)
- [CrearFojaDeMedicion](CrearFojaDeMedicion.md)
- [FormValidationError](../../../core/models/FormValidationError.md)
