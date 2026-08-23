---
symbol: AddRelatedPermissionMixin
kind: class
module: carga/forms/mixins.py
lines: 1-20
signature_hash: sha1:70ed9da8850e4a9795ee416c71d82b46a385a426
authored: true
---

# AddRelatedPermissionMixin

**Módulo:** `carga/forms/mixins.py` (líneas 1-20)

## Propósito

Complemento de [AddRelatedWidgetMixin](../../views/ajaxviews/AddRelatedWidgetMixin.md): oculta el
botón "+" de un campo select2 si el usuario actual no tiene el permiso `add_<modelo>` del
modelo relacionado — así el botón nunca ofrece una acción que de todos modos fallaría por
permisos. Requiere que la vista instancie el form pasando `user=request.user`
(`core.mixins.UserKwargsMixin` es el mecanismo estándar para eso en este proyecto).

Recorre todos los campos del form buscando widgets con `add_related_url_name` seteado
(la marca que deja `AddRelatedWidgetMixin`), y en cada uno resuelve el modelo relacionado
desde `field.queryset.model` para chequear el permiso correspondiente.

## Firma

```python
class AddRelatedPermissionMixin:
```

## Uso real

`class PolizaForm(AddRelatedPermissionMixin, forms.ModelForm)`, `class ObraForm(AddRelatedPermissionMixin, forms.ModelForm)`.

## Ver también

- [AddRelatedWidgetMixin](../../views/ajaxviews/AddRelatedWidgetMixin.md)
- [PolizaForm](PolizaForm.md)
- [ObraForm](ObraForm.md)
