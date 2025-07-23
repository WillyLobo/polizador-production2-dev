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
        if self.request.POST:
            context['group_formset'] = self.formset_name(self.request.POST, instance=self.object)
            # por que esta vergación tiene que estar acá para que los errores del formset se muestren correctamente?
            context.get('group_formset').errors
        else:
            context['group_formset'] = self.formset_name(instance=self.object)
        return context

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except AttributeError:
            self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_name(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
	
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except AttributeError:
            self.object = None

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_name(self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid() and formset.is_valid():
            form.save()
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        if self.view_type == "create":
            """If the form is valid, save the associated model."""
            self.object = form.save()
            if formset.is_valid():
                response = super().form_valid(form)
                formset.instance = self.object
                formset.save()
                return response
            else:
                return super().form_invalid(form=form, formset=formset)
        elif self.view_type == "update":
            if formset.is_valid():
                response = super().form_valid(form)
                formset.instance = self.object
                formset.save()
                return response
            else:
                return super().form_invalid(form=form, formset=formset)
            
    def form_invalid(self, form, formset):
        """
        Renders the response based on the context data with the form and formset if the form is invalid.

        :param form: The form instance.
        :param formset: The formset instance.
        :return: The response rendered based on the context data.
        """
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
