from django.contrib.admin.utils import NestedObjects
from django.http import JsonResponse
from django.utils.text import capfirst
from django.utils.encoding import force_str

class UserKwargsMixin:
    """Pasa el usuario actual al form principal (lo consume AddRelatedPermissionMixin en
    carga/forms/mixins.py para decidir si mostrar el boton "+" de un select2 FK)."""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class UserFormsetKwargsMixin:
    """Como UserKwargsMixin, pero para el form de un formset (FormsetViewMixin en
    secretariador/forms/mixins.py). Usar solo si ese form tambien tiene
    AddRelatedPermissionMixin (o acepta `user=` de otra forma): si el form del formset
    no acepta ese kwarg, agregarlo rompe con un TypeError."""

    def get_formset_kwargs(self):
        return {"user": self.request.user}

class PopupCreateMixin:
    """Permite usar un CreateView dentro del modal de "+ agregar" de un select2 FK
    (ver AddRelatedWidgetMixin en carga/views/ajaxviews.py).

    Cuando la request trae `_popup=1` (agregado por select2-add-related.js), sirve un
    template minimo en vez de la pagina completa y, al guardar, devuelve JSON
    {id, text} en lugar de redirigir.
    """

    popup_template_name = "generic/popup_create_form.html"
    popup_form_partial = None
    """Partial ya usado por la pagina completa de este modelo (ej.
    "partials/aseguradora-form-partial.html"). Si no se define, el popup
    renderiza el form con `form.as_div`."""

    def is_popup(self):
        return bool(self.request.GET.get("_popup") or self.request.POST.get("_popup"))

    def get_template_names(self):
        if self.is_popup():
            return [self.popup_template_name]
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.is_popup():
            context["popup_form_partial"] = self.popup_form_partial
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.is_popup():
            return JsonResponse({"id": self.object.pk, "text": str(self.object)})
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.is_popup():
            response.status_code = 400
        return response

def get_deleted_objects(objs):
    collector = NestedObjects(using="default")
    collector.collect(objs)

    def format_callback(obj):
        opts = obj._meta
        no_edit_link = "%s: %s" % (capfirst(opts.verbose_name), force_str(obj))

        return no_edit_link
    
    to_delete = collector.nested(format_callback)
    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {model._meta.verbose_name_plural: len(objs) for model, objs in collector.model_objs.items()}

    return to_delete, model_count, protected