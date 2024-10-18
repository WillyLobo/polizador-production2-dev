from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView
from django.http import HttpResponse
from fallout.models import CharFallout
from fallout.forms import PlanillaFalloutForm

# def skill_up(habilidad_total, habilidad_skill, habilidad_puntos):
#     for _ in range(habilidad_puntos):
#         if habilidad_total <= 0:
#             return 0, 0
        
#         incrementos = [
#             (200, 1/6),
#             (175, 1/5),
#             (150, 1/4),
#             (125, 1/3),
#             (100, 1/2),
#             (0, 1)
#         ]
        
#         for limite, incremento in incrementos:
#             if habilidad_total > limite:
#                 habilidad_skill += incremento
#                 break
        
#         habilidad_total += incremento
#     return habilidad_total, habilidad_skill

def skill_up(habilidad_total, habilidad_puntos, tagged):
    habilidad_total = float(habilidad_total)
    habilidad_puntos = float(habilidad_puntos)
    """
    Corcky:
        Melee = 46 base * 2 tageado (92)
        Puntos por nivel = 11
        Nivel = 18
        Puntos de Habilidad = 11 * 18= 198
    """
    for _ in range(int(habilidad_puntos)):
        if habilidad_total <= 0:
            return 0, 0
        
        incrementos = [
            (200, 1/6),
            (175, 1/5),
            (150, 1/4),
            (125, 1/3),
            (100, 1/2),
            (0, 1)
        ]
        
        for limite, incremento in incrementos:
            if habilidad_total > limite:
                if tagged == True:
                    habilidad_total += incremento*2
                else:
                    habilidad_total += incremento
                break
        
    return habilidad_total

def skill_test(request):
	template_name = "skill_check.html"

	return render(request, template_name, {})

def skill_check(request):
    if request.method == 'POST':
        habilidad_total = float(request.POST.get("habilidad_total"))
        habilidad_puntos = int(request.POST.get("habilidad_puntos"))
        tagged = request.POST.get("tagged")
        habilidad_total = skill_up(habilidad_total, habilidad_puntos, tagged)
        return render(request, 'partials/skill_partial.html', {'habilidad_total': habilidad_total})
    else:
        return HttpResponse("Error")