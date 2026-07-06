from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic


@method_decorator(login_required, name="dispatch")
class ManualObraPlanFojaView(generic.TemplateView):
    template_name = "ayuda/manual-obra-plan-foja.html"


@method_decorator(login_required, name="dispatch")
class ManualCertificadosView(generic.TemplateView):
    template_name = "ayuda/manual-certificados.html"
