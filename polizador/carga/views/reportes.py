from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from carga.models import Certificado, Obra, Localidad, Empresa, Programa, CertificadoRubro, Uvi
from carga.forms.certificadoforms import *
from django.db.models import Q, FilteredRelation, Subquery, OuterRef, Sum, F
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page
from datetime import datetime, timedelta

@method_decorator(login_required, name="dispatch")
class CrearReporteCertificadoPorMes(PermissionRequiredMixin, generic.TemplateView) :
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.view_certificado"
	template_name = "reportes/crear-reportecertificadopormes.html"

@method_decorator(login_required, name="dispatch")
class VerReporteCertificadoPorMes(PermissionRequiredMixin, generic.ListView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.view_certificado"

	model = Certificado
	context_object_name = "object_list"
	template_name = "reportes/ver-reportecertificadopormes.html"
	
	def get_queryset(self):
		mes_list = self.request.GET.getlist("mes")
		ano = self.request.GET.get("ano")

		certificados = Certificado.objects.filter(certificado_fecha_carga__year=ano,certificado_fecha_carga__month__in=mes_list).order_by("certificado_obra__obra_programa").prefetch_related("certificado_obra").select_related("certificado_obra__obra_empresa","certificado_obra__obra_programa")
		
		return certificados

@method_decorator(login_required, name="dispatch")
class CrearReporteView(PermissionRequiredMixin, generic.TemplateView) :
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.view_certificado"
	template_name = "reportes/crear-reporteobra.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		localidades = Localidad.objects.all()
		empresas = Empresa.objects.all()
		programas = Programa.objects.all()
		rubros = CertificadoRubro.objects.all()
		
		context["localidades"] = localidades
		context["empresas"] = empresas
		context["programas"] = programas
		context["rubros"] = rubros

		return context

@method_decorator(login_required, name="dispatch")
@method_decorator(cache_page(60*15), name="dispatch")
class VerReporteView(PermissionRequiredMixin, generic.ListView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.view_certificado"

	model = Obra
	context_object_name = "object_list"
	template_name = "reportes/ver-reporteobra.html"
	
	def get_queryset(self):
		localidad = self.request.GET.getlist("localidad")
		programa = self.request.GET.getlist("programa")
		empresa = self.request.GET.getlist("empresa")
		pctavance = self.request.GET.get("pctavance")
		tipodefiltro = self.request.GET.get("tipodefiltro")
		rubro = self.request.GET.get("rubro")
		financiamiento = self.request.GET.get("financiamiento")
		# print(self.request.GET)
		# object_list = Obra.objects.all()
		
		# Crea un query vacio, para anexarle los subsiguientes querys.
		objects_query = Q()
		try:
			localidad_query = Q()
			for l in localidad:
				localidad_query |= Q(obra_localidad_m=l)
		except IndexError:
			pass
		try:
			empresa_query = Q()
			for e in empresa:
				empresa_query |= Q(obra_empresa__id=e)
		except IndexError:
			pass
		try:
			programa_query = Q()
			for p in programa:
				programa_query |= Q(obra_programa__id=p)
		except IndexError:
			pass
		
		# Generar un filtro previo a fin de acortar el chequeo sobre la base de datos de los acumulados porcentuales.
		pre_listado = Obra.objects.all().filter(localidad_query, empresa_query, programa_query, objects_query)
		
		# Filtrado de avances porcentuales.
		# Tipo de filtro: 1 = Igual a - 2 = Menor a - 3 = Mayor a
		try:
			if tipodefiltro == "1":
				mas_nuevo = pre_listado.annotate(pct=Sum(F("certificado__certificado_mes_pct"))).filter(pct__exact=pctavance)
				pre_listado = mas_nuevo
			elif tipodefiltro == "2":
				mas_nuevo = pre_listado.annotate(pct=Sum(F("certificado__certificado_mes_pct"))).filter(pct__lt=pctavance)
				pre_listado = mas_nuevo
			elif tipodefiltro == "3":
				mas_nuevo = pre_listado.annotate(pct=Sum(F("certificado__certificado_mes_pct"))).filter(pct__gt=pctavance)
				pre_listado = mas_nuevo
			else:
				pre_listado = pre_listado
		except ValidationError:
				pre_listado = pre_listado

		# Rubro Values:
		# value="1" Vivienda
		# value="2" Infraestructura Frentista
		# value="3" Terreno
		# value="4" Redeterminación
		# value="5" Nexos y Redes
		# value="8" Reconocimiento de Trabajos
		# value="9" Ampliación de Contrato
		
		# Monstruosidad asquerosa para filtrar por rubro de contrato.
		# Genera una lista "cmid" con los id del modelo Obra, tomados desde el modelo "CertificadoRubro", sobre los que filtra los id.
		cmid = []
		try:
			for r in rubro:
				contrato = pre_listado.filter(contrato__contrato_descripcion="Contrato Base")
				for cset in contrato:
					try:
						c = cset.contrato_set.first().contratomonto_set
						c = c.filter(contratomonto_rubro=r).last()
						try:
							cmid.append(c.contratomonto_contrato.contrato_obra.id)
						except TypeError:
							pass
					except AttributeError:
						pass
			pre_listado=pre_listado.filter(id__in=cmid)
		except ValidationError:
			pass
		except TypeError:
			pass

		
		listado = pre_listado
		return listado

@method_decorator(login_required, name="dispatch")
class CrearListaUvi(PermissionRequiredMixin, generic.ListView):
	login_url = "/"
	redirect_field_name = "login"
	permission_required = "carga.view_certificado"

	model = Uvi
	title = "Valor UVI"
	context_object_name = "object_list"
	template_name = "reportes/crear-lista-uvi.html"
	
	def get_queryset(self, **kwargs):
		"""
		Returns a queryset of Uvi objects based on the dates provided in the request.GET parameters. 
		If no parameters are provided, it fetches Uvi objects within a default date range and orders them by date.
		If parameters are provided, it fetches Uvi objects within the specified date range and orders them by date.
		
		:param kwargs: Additional keyword arguments
		:return: A queryset of Uvi objects filtered and ordered based on the request parameters
		"""		
		if not self.request.GET:
			fecha_final = datetime.today()
			fecha_final += timedelta(days=10)
			fecha_inicial = fecha_final - timedelta(days=60)
			uvi = Uvi.objects.filter(uvi_fecha__range=[fecha_inicial,fecha_final]).order_by("-uvi_fecha")
		elif self.request.GET:
			fecha_final = self.request.GET.get("fecha_final")
			fecha_final = datetime.strptime(fecha_final, "%d/%m/%Y")
			fecha_inicial = self.request.GET.get("fecha_inicial")
			fecha_inicial = datetime.strptime(fecha_inicial, "%d/%m/%Y")
			uvi = Uvi.objects.filter(uvi_fecha__range=[fecha_inicial, fecha_final]).order_by("-uvi_fecha")
		return uvi

	def get_title(self):
		return self.title
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = self.get_title()
		return context
