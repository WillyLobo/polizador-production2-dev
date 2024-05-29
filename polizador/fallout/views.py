from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView
from fallout.models import CharFallout
from fallout.forms import PlanillaFalloutForm

@method_decorator(login_required, name="dispatch")
class PlanillaFalloutDetailView(PermissionRequiredMixin, UpdateView):
    model = CharFallout
    template_name = "planilla-fallout.html"
    form_class = PlanillaFalloutForm
    permission_required = "fallout.change_charfallout"

@method_decorator(login_required, name="dispatch")
class PlanillaFalloutCreateView(PermissionRequiredMixin, CreateView):
    model = CharFallout
    template_name = "planilla-fallout.html"
    form_class = PlanillaFalloutForm
    permission_required = "fallout.add_charfallout"

