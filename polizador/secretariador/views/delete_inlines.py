from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views import generic
from secretariador.models import ComisionadoSolicitud
from secretariador.forms.solicitudform import *
from carga.views.generics import get_deleted_objects
from django.contrib import messages

@login_required
@permission_required('secretariador.delete_comisionadosolicitud')
def delete_comisionadosolicitud(request, pk):
    try:
        comisionado = ComisionadoSolicitud.objects.get(id=pk)
    except ComisionadoSolicitud.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('secretariador:update-solicitud', pk=comisionado.comisionadosolicitud_foreign.id)

    comisionado.delete()
    messages.success(
            request, 'Comisionado deleted successfully'
            )
    return redirect('secretariador:update-solicitud', pk=comisionado.comisionadosolicitud_foreign.id)