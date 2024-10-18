from django.urls import path
from fallout.views.planillaviews import *
from fallout.views.generator import *
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

app_name = "fallout"

urlpatterns = [
    path("", login_required(TemplateView.as_view(template_name='home/index.html')), name="fallout-home"),
    path("planilla/create/", PlanillaFalloutCreateView.as_view(), name="planilla-fallout-create"),
    path("planilla/update/<pk>/", PlanillaFalloutUpdateView.as_view(), name="planilla-fallout-update"),
    # path("planilla/<pk>/", PlanillaFalloutDetailView.as_view(), name="planilla-fallout-detail"),
    path("list/", PlanillaFalloutListView.as_view(), name="planilla-fallout-list"),
    # path("skill_test/", skill_test, name="skill-test"),
    # path("skill_check/", skill_check, name="skill-check"),
]