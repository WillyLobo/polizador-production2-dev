from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.safestring import SafeString
from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy

class BaseFormMixin(object):
    required_css_class = "required"

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))
    
class ColumnFormMixin(object):

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", f"<div class='col column-{self.prefix}'>"))
    
class FormsetViewMixin(generic.View):
    formset_name = None
    view_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formset = kwargs.get('formset')
        if formset is None:
            formset = self.formset_name(instance=self.object)
        context['group_formset'] = formset
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object() if self.view_type == "update" else None

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_name(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() if self.view_type == "update" else None

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_name(self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid() and formset.is_valid():
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
