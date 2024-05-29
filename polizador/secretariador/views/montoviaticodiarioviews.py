from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import InstrumentosLegalesDecretos, MontoViaticoDiario
from secretariador.forms.montoviaticodiarioform import *
from secretariador.forms.instrumentoslegalesform import InstrumentosLegalesDecretosForm
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class CrearMontoViaticoDiario(PermissionRequiredMixin, generic.CreateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.add_montoviaticodiario"

	model = InstrumentosLegalesDecretos
	template_name = "montoviaticodiario/crear-montoviaticodiario.html"
	form_class = InstrumentosLegalesDecretosForm
	success_url = reverse_lazy("secretariador:crear-montoviaticodiario")
	
	title = "Crear Monto Viatico Diario"

	def get_title(self):
		return self.title

	def get_context_data(self, **kwargs):
		context = super(CrearMontoViaticoDiario, self).get_context_data(**kwargs)

		context['montoviaticodiarioformset'] = MontoViaticoDiarioFormset(instance=self.object)
		return context

	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		montoviaticodiarioformset = MontoViaticoDiarioFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, montoviaticodiarioformset = montoviaticodiarioformset))

	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		montoviaticodiarioformset = MontoViaticoDiarioFormset(self.request.POST, instance=self.object)
		if form.is_valid() and montoviaticodiarioformset.is_valid():
			form.save()
			return self.form_valid(form, montoviaticodiarioformset)
		else:
			return self.form_invalid(form, montoviaticodiarioformset)

	def form_valid(self, form, formset):
		self.object = form.save()
		if formset.is_valid():
			response = super().form_valid(form)
			formset.instance = self.object
			formset.save()
			return response
		else:
			return super().form_invalid(form, formset)
	
	def form_invalid(self, form, montoviaticodiarioformset):
		return self.render_to_response(self.get_context_data(form=form, montoviaticodiarioformset = montoviaticodiarioformset))

@method_decorator(login_required, name="dispatch")
class UpdateMontoViaticoDiario(PermissionRequiredMixin, generic.UpdateView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.change_montoviaticodiario"

	model = InstrumentosLegalesDecretos
	template_name = "montoviaticodiario/update-montoviaticodiario.html"
	form_class = InstrumentosLegalesDecretosForm
	success_url = reverse_lazy("secretariador:lista-decretos")
	
	def get_context_data(self, **kwargs):
		context = super(UpdateMontoViaticoDiario, self).get_context_data(**kwargs)

		context["montoviaticodiarioformset"] = MontoViaticoDiarioFormset(instance=self.object)
		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		montoviaticodiarioformset = MontoViaticoDiarioFormset(instance=self.object)
		return self.render_to_response(self.get_context_data(form=form, montoviaticodiarioformset = montoviaticodiarioformset))
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		montoviaticodiarioformset = MontoViaticoDiarioFormset(self.request.POST, instance=self.object)
		if form.is_valid() and montoviaticodiarioformset.is_valid():
			form.save()
			return self.form_valid(form, montoviaticodiarioformset)
		else:
			return self.form_invalid(form, montoviaticodiarioformset)
		
	def form_valid(self, form, montoviaticodiarioformset):
		formset = montoviaticodiarioformset.save(commit=False)
		for field in formset:
			field.montoviaticodiario_decreto_reglamentario = self.object
			field.save()
		return redirect(reverse_lazy("secretariador:lista-decretos"))
	
	def form_invalid(self, form, montoviaticodiarioformset):
		"""
		Renders the response based on the context data with the form and formset if the form is invalid.

		:param form: The form instance.
		:param comisionadosformset: The comisionados formset instance.
		:return: The response rendered based on the context data.
		"""
		return self.render_to_response(self.get_context_data(form=form, montoviaticodiarioformset=montoviaticodiarioformset))


@method_decorator(login_required, name="dispatch")
class EliminarMontoViaticoDiario(PermissionRequiredMixin, generic.DeleteView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "secretariador.delete_montoviaticodiario"

	model = MontoViaticoDiario
	template_name = "generic/confirm_delete.html"
	success_url = reverse_lazy("secretariador:lista-decretos")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		deletable_objects, model_count, protected = get_deleted_objects([self.object])
		context["deletable_objects"] = deletable_objects
		context["model_count"] = dict(model_count).items()
		context["protected"] = protected
		return context