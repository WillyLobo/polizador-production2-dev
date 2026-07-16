from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy

from core.deletion import get_deleted_objects

class UserKwargsMixin:
    """Pasa el usuario actual al form principal (lo consume AddRelatedPermissionMixin en
    carga/forms/mixins.py para decidir si mostrar el boton "+" de un select2 FK)."""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class UserFormsetKwargsMixin:
    """Como UserKwargsMixin, pero para el form de un formset (FormsetViewMixin en
    core/mixins.py). Usar solo si ese form tambien tiene
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

class BaseFormMixin(object):
    required_css_class = "required"

class DeleteRelatedObjectsMixin:
    """Para DeleteView: muestra los objetos relacionados que se borrarian en
    cascada (o que bloquean el borrado por ser PROTECT) y, si el usuario
    confirma igual, atrapa el ProtectedError que lanza .delete() en ese caso
    en lugar de dejarlo propagar como error 500."""

    protected_error_message = "No se puede eliminar porque tiene relaciones protegidas asociadas."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context["deletable_objects"] = deletable_objects
        context["model_count"] = dict(model_count).items()
        context["protected"] = protected
        return context

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, self.protected_error_message)
            return redirect(self.get_success_url())

class FormsetViewMixin(generic.View):
    formset_name = None
    view_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formset = kwargs.get('formset')
        if formset is None:
            formset = self.formset_name(instance=self.object, form_kwargs=self.get_formset_kwargs())
        context['group_formset'] = formset
        return context

    def get_formset_kwargs(self):
        """Hook for subclasses: extra `form_kwargs` forwarded to every form of the
        formset (ej. `{"user": self.request.user}` para AddRelatedPermissionMixin)."""
        return {}

    def prepare_formset(self, formset):
        """Hook for subclasses to set per-form `initial` values right after construction.

        Must happen here, before `is_valid()`/`full_clean()` runs: for forms backed by an
        existing instance (a `ModelFormSet`'s "initial" forms), passing `initial=` to the
        formset constructor is silently ignored, and mutating `form.initial` after cleaning
        has no visible effect either, since Django caches each form's BoundFields the first
        time they're accessed during cleaning.
        """
        pass

    def get(self, request, *args, **kwargs):
        self.object = self.get_object() if self.view_type == "update" else None

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_name(instance=self.object, form_kwargs=self.get_formset_kwargs())
        self.prepare_formset(formset)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() if self.view_type == "update" else None

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_name(
            self.request.POST, self.request.FILES, instance=self.object,
            form_kwargs=self.get_formset_kwargs(),
        )
        self.prepare_formset(formset)
        # No usar "and": evaluarlos por separado para que formset.is_valid() corra siempre,
        # incluso si `form` ya es inválido. De lo contrario formset nunca llama a full_clean()
        # y form.instance.<fk> queda sin completar al renderizar la tabla de items.
        form_is_valid = form.is_valid()
        formset_is_valid = formset.is_valid()
        if form_is_valid and formset_is_valid:
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        if self.view_type not in ("create", "update"):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__}.view_type must be 'create' or 'update', got {self.view_type!r}"
            )
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        """
        Renders the response based on the context data with the form and formset if the form is invalid.

        :param form: The form instance.
        :param formset: The formset instance.
        :return: The response rendered based on the context data.
        """
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
