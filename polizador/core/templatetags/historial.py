from django import template
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse

from core.history import can_view_history, history_manager

register = template.Library()


@register.simple_tag(takes_context=True)
def historial_sidebar(context):
    """Pestaña de historial para el `object` de la vista (DetailView/UpdateView/DeleteView),
    si su modelo tiene simple_history y el usuario puede verlo. Las vistas que no exponen
    `object` pueden indicar cuál mostrar con `historial_object`."""
    obj = context.get("historial_object") or context.get("object")
    request = context.get("request")
    if not isinstance(obj, models.Model) or obj.pk is None or request is None:
        return ""
    model = type(obj)
    if history_manager(model) is None or not can_view_history(request.user, model):
        return ""
    url = reverse("historial", kwargs={
        "app_label": model._meta.app_label,
        "model_name": model._meta.model_name,
        "pk": obj.pk,
    })
    return render_to_string("partials/historial-sidebar.html", {"historial_url": url}, request=request)
