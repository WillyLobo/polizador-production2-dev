from django.urls import path
from fallout.views import PlanillaFalloutCreateView, PlanillaFalloutDetailView

app_name = "fallout"

urlpatterns = [
    path("planilla/create/", PlanillaFalloutCreateView.as_view(), name="planilla-fallout-create"),
    path("planilla/<pk>/", PlanillaFalloutDetailView.as_view(), name="planilla-fallout-detail"),
]