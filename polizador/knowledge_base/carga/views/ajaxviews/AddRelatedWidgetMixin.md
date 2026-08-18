---
symbol: AddRelatedWidgetMixin
kind: class
module: carga/views/ajaxviews.py
lines: 8-32
signature_hash: sha1:c078c4feaee97771e4f27ba55d9e892118f25034
authored: true
---

# AddRelatedWidgetMixin

**Módulo:** `carga/views/ajaxviews.py` (líneas 8-32)

## Propósito

Mixin que agrega un botón "+" al lado de un `<select>` de select2: al hacer click abre
(en un modal Bootstrap) el form de alta del modelo relacionado, y al guardar inserta el
objeto recién creado como opción ya seleccionada en el select de origen — sin recargar la
página ni perder el resto del formulario que se estaba completando.

Requiere `add_related_url_name` (el nombre de URL del `CreateView` correspondiente, que
a su vez debe usar `PopupCreateMixin` — ver `core/mixins.py` — para saber que tiene que
devolver el objeto creado en vez de redirigir). `add_related_allowed` puede ponerlo en
`False` `AddRelatedPermissionMixin` (`carga/forms/mixins.py`) para ocultar el botón según
el permiso `add_<modelo>` del usuario actual — el botón nunca se muestra si el usuario no
podría completar el alta de todos modos.

## Firma

```python
class AddRelatedWidgetMixin:
```

## Uso real

`carga/static/carga/js/select2-add-related.js` (cargado globalmente en `templates/base.html`) es el JS que engancha el click del botón `.select2-add-related` con el modal `#addRelatedModal`.

## Ver también

- [PlanDependentWidgetMixin](PlanDependentWidgetMixin.md)
- [programawidget](programawidget.md) — uno de los widgets que lo usa.
