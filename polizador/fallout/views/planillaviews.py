from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from fallout.models import CharFallout
from fallout.forms import PlanillaFalloutForm, PlanillaFalloutCreateForm, PlanillaFalloutUpdateForm
from fallout.views.generator import skill_up

@login_required
def skill_test(request):
	template_name = "skill_check.html"

	return render(request, template_name, {})

@login_required
def skill_check(request):
    if request.method == 'POST':
        habilidad_total = float(request.POST.get("habilidad_total"))
        habilidad_puntos = int(request.POST.get("habilidad_puntos"))
        habilidad_total = skill_up(habilidad_total, habilidad_puntos)
        return render(request, 'partials/skill_partial.html', {'habilidad_total': habilidad_total})
    else:
        return HttpResponse("Error")

@method_decorator(login_required, name="dispatch")
class PlanillaFalloutListView(PermissionRequiredMixin, ListView):
    model = CharFallout
    template_name = "planilla-list-fallout.html"
    permission_required = "fallout.view_charfallout"

    def get_queryset(self):
        return self.model.objects.filter(nombreJugador=self.request.user)
# @method_decorator(login_required, name="dispatch")
# class PlanillaFalloutDetailView(PermissionRequiredMixin, UpdateView):
#     model = CharFallout
#     template_name = "planilla-fallout.html"
#     form_class = PlanillaFalloutForm
#     permission_required = "fallout.change_charfallout"

@method_decorator(login_required, name="dispatch")
class PlanillaFalloutCreateView(PermissionRequiredMixin, CreateView):
    model = CharFallout
    template_name = "planilla-create-fallout.html"
    form_class = PlanillaFalloutCreateForm
    permission_required = "fallout.add_charfallout"
    success_url = reverse_lazy("fallout:planilla-fallout-create")

@method_decorator(login_required, name="dispatch")
class PlanillaFalloutUpdateView(PermissionRequiredMixin, UpdateView):
    model = CharFallout
    template_name = "planilla-update-fallout.html"
    form_class = PlanillaFalloutUpdateForm
    permission_required = "fallout.add_charfallout"
    # success_url = reverse_lazy("fallout:planilla-fallout-update")

    # def form_valid(self, form):
    #     instance = form.instance
    #     instance.apTotal = instance.apBase + instance.apMod
    #     instance.secTotal = instance.secBase + instance.secMod
    #     instance.danoMeleeTotal = instance.danoMeleeBase + instance.danoMeleeMod
    #     instance.probCriticoTotal = instance.probCriticoBase + instance.probCriticoMod
    #     instance.ratioCuracionTotal = instance.ratioCuracionBase + instance.ratioCuracionMod
    #     instance.capCargaTotal = instance.capCargaBase + instance.capCargaMod
    #     instance.resVenenoTotal = instance.resVenenoBase + instance.resVenenoMod
    #     instance.resRadiacionTotal = instance.resRadiacionBase + instance.resRadiacionMod
    #     instance.resElectricidadTotal = instance.resElectricidadBase + instance.resElectricidadMod
    #     instance.implanteTotal = instance.implanteBase + instance.implanteMod
    #     form.save()
    #     print(instance.apTotal)
    #     return super().form_valid(form)

    def get_success_url(self):
        char_id = self.object.id #gets id from created object
        return reverse_lazy('fallout:planilla-fallout-update', kwargs={"pk": char_id})