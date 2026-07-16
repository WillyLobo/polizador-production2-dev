class AddRelatedPermissionMixin:
    """Para ModelForms con campos cuyo widget usa AddRelatedWidgetMixin: oculta el boton
    "+" si el usuario no tiene el permiso add_<modelo> del modelo relacionado.

    Requiere que la vista pase `user=request.user` al instanciar el form
    (ver core.mixins.UserKwargsMixin).
    """

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is None:
            return
        for field in self.fields.values():
            widget = field.widget
            if not getattr(widget, "add_related_url_name", None):
                continue
            model = getattr(getattr(field, "queryset", None), "model", None)
            widget.add_related_allowed = bool(
                model and user.has_perm(f"{model._meta.app_label}.add_{model._meta.model_name}")
            )
