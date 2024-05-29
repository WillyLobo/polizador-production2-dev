from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.template import loader, TemplateDoesNotExist
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from secretariador.models import Comisionado, Organigrama, Vehiculo, Solicitud
from .forms.solicitudform import SolicitudForm
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg
from carga.views.generics import get_deleted_objects
import locale
from django.contrib.auth import logout

