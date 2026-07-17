from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import EncabezadoDocumento
from secretariador.forms.encabezadoform import EncabezadoDocumentoForm


@method_decorator(login_required, name="dispatch")
class ActualizarEncabezado(PermissionRequiredMixin, generic.CreateView):
	permission_required = "secretariador.add_encabezadodocumento"

	model = EncabezadoDocumento
	template_name = "encabezado/actualizar-encabezado.html"
	form_class = EncabezadoDocumentoForm
	success_url = reverse_lazy("secretariador:actualizar-encabezado")

	title = "Actualizar Encabezado"

	def get_title(self):
		return self.title

	def form_valid(self, form):
		form.instance.encabezadodocumento_subido_por = self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["historial"] = EncabezadoDocumento.objects.all()[:10]
		return context
