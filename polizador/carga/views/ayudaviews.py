from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic


@method_decorator(login_required, name="dispatch")
class ManualObraPlanFojaView(generic.TemplateView):
    template_name = "ayuda/manual-obra-plan-foja.html"


@method_decorator(login_required, name="dispatch")
class ManualCertificadosView(generic.TemplateView):
    template_name = "ayuda/manual-certificados.html"


@method_decorator(login_required, name="dispatch")
class ManualReprogramacionView(generic.TemplateView):
    template_name = "ayuda/manual-reprogramacion.html"


@method_decorator(login_required, name="dispatch")
class ManualTextosResolucionView(generic.TemplateView):
    template_name = "ayuda/manual-textos-resolucion.html"

    def get_context_data(self, **kwargs):
        from carga.resolucion_texto import FILTROS_DOC, VARIABLES

        context = super().get_context_data(**kwargs)
        # La tabla de variables sale del mismo catálogo que alimenta la paleta del
        # editor: una sola fuente de verdad, para que el manual no se desactualice.
        context["variables"] = VARIABLES
        context["filtros_doc"] = FILTROS_DOC
        return context
