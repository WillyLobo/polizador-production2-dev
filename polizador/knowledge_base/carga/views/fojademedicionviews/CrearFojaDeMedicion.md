---
symbol: CrearFojaDeMedicion
kind: class
module: carga/views/fojademedicionviews.py
lines: 50-187
signature_hash: sha1:8ecae47e4a1ef19d4f68bc3a9878b8da4e0da516
authored: true
---

# CrearFojaDeMedicion

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 50-187) · hereda de `LogInvalidFormMixin, PermissionRequiredMixin, FormsetViewMixin, generic.CreateView`

## Propósito

La vista más compleja del módulo `fojademedicionviews`: sobreescribe `get`/`post` en vez
de apoyarse en el flujo estándar de `CreateView`, porque el formset de items
(`FojaDeMedicionItemFormset`) tiene que armarse dinámicamente según el Rubro elegido — una
fila por `PlanDeTrabajosItem` de ese rubro, no un número fijo de filas
(`build_foja_item_formset_class(extra=items.count())`). En el `GET`, si viene
`?rubro=<id>`, prellena cada fila con el `%` anterior de ese item
(`FojaDeMedicion.anterior_items_map`) para que el usuario vea de entrada cuánto llevaba
acumulado sin tener que ir a buscarlo.

Además del formset de items, maneja un segundo formset independiente de fotos
(`FojaDeMedicionFotoFormset`) y, si la Foja resulta ser `foja_legacy`, vincula los
Certificados elegidos en el campo `foja_legacy_certificados` (ver
[certificadolegacywidget](../ajaxviews/certificadolegacywidget.md)) seteándoles
`certificado_foja` después de guardar. También setea `PlanDeTrabajos.trabajos_fecha_inicio`
la primera vez que se carga (si el form trae ese dato y el Plan todavía no lo tiene).

Por tener `post()` totalmente custom (no llama a `self.form_invalid()`), es el ejemplo
citado en el propio docstring de `LogInvalidFormMixin` (`core/mixins.py`, fuera del
alcance de esta base de conocimiento — no es `models.py`/`views.py`/`forms.py`) para el
caso que necesita invocar `self._log_form_debug(form, formset, foto_formset)` a mano en
el branch inválido — el hook automático del mixin (`form_invalid()`) nunca se dispara acá.

## Firma

```python
class CrearFojaDeMedicion(LogInvalidFormMixin, PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
```

## Uso real

```python
# carga/views/fojademedicionviews.py:140 (post)
self.object = form.save()
self._save_fecha_inicio(form)
self._vincular_certificados_legacy(form)
formset.instance = self.object
formset.save()          # -> cada FojaDeMedicionItem.save() + cascada (ver la señal)
foto_formset.instance = self.object
foto_formset.save()
```

## Ver también

- [FojaDeMedicion](../../models/FojaDeMedicion.md)
- [FojaDeMedicionItem](../../models/FojaDeMedicionItem.md)
- [recalcular_acumulado_fojas_siguientes](../../signals/recalcular_acumulado_fojas_siguientes.md)
- [certificadolegacywidget](../ajaxviews/certificadolegacywidget.md)
- [FormValidationError](../../../core/models/FormValidationError.md)
