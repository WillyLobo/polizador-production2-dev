from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy

class BaseFormMixin(object):
    required_css_class = "required"

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
