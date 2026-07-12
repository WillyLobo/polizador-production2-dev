from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from carga.models import Obra, FojaDeMedicion
from personalizador.models import Agente
from django.views import generic
from carga.views.generics import get_deleted_objects

@method_decorator(login_required, name="dispatch")
class InspeccionHomeView(generic.ListView):
    template_name = "index.html"
    model = Obra
    context_object_name = "obras"

    def get_queryset(self):
        agente = getattr(self.request.user, "agente", None)
        if agente is not None and self.request.user.groups.filter(name="inspeccion").exists():
            return Obra.objects.filter(obra_inspector=agente)
        else:
            return Obra.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agente = getattr(self.request.user, "agente", None)
        if agente is None:
            context["fojas"] = FojaDeMedicion.objects.none()
        else:
            context["fojas"] = FojaDeMedicion.objects.filter(
                foja_inspector=agente
            ).select_related("foja_rubro__rubro_plan__trabajos_obra").order_by("-foja_periodo")

        if self.request.user.groups.filter(name="certificadores").exists():
            context["fojas_sin_certificado"] = FojaDeMedicion.objects.filter(
                certificado__isnull=True
            ).select_related("foja_rubro__rubro_plan__trabajos_obra").order_by("-foja_periodo")
        return context




