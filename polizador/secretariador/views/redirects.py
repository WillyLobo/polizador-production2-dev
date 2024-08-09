from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def redirect_decretos(request):
	template_name = "generic/redirect_decretos.html"

	return render(request, template_name, {})

@login_required
def redirect_solicitudes(request):
	template_name = "generic/redirect_solicitudes.html"

	return render(request, template_name, {})
