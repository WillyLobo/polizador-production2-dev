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
def planilla_test(request):
	template_name = "planilla-create-dnd5.html"

	return render(request, template_name, {})

# Calculations:
# Stat Modifiers = math.floor((Stat - 10) / 2)
# Saving throws modifier = save + stat modifier + proficiency bonus(if any)
# Skill modifier = skill + stat modifier + proficiency bonus(if any)