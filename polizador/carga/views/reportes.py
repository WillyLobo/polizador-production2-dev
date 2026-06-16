from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from carga.models import Certificado, Obra, Localidad, Empresa, Programa, CertificadoRubro, Uvi
from django.db.models import Q, FilteredRelation, Subquery, Sum, F
from django.core.exceptions import ValidationError
from django.core.management import call_command
from datetime import datetime, timedelta

@method_decorator(login_required, name="dispatch")
class CrearReporteCertificadoPorMes(PermissionRequiredMixin, generic.TemplateView) :
	permission_required = "carga.view_certificado"
	template_name = "reportes/crear-reportecertificadopormes.html"

@method_decorator(login_required, name="dispatch")
class VerReporteCertificadoPorMes(PermissionRequiredMixin, generic.ListView):
	permission_required = "carga.view_certificado"

	model = Certificado
	context_object_name = "object_list"
	template_name = "reportes/ver-reportecertificadopormes.html"
	
	def get_queryset(self):
		mes_list = self.request.GET.getlist("mes")
		ano = self.request.GET.get("ano")
		certificados = Certificado.objects.filter(certificado_fecha__year=ano, certificado_fecha__month__in=mes_list).order_by("certificado_obra__obra_programa").prefetch_related("certificado_obra").select_related("certificado_obra__obra_empresa", "certificado_obra__obra_programa")
		return certificados

@method_decorator(login_required, name="dispatch")
class CrearReporteObraView(PermissionRequiredMixin, generic.ListView):
	permission_required = "carga.view_certificado"
	model = Obra
	context_object_name = "object_list"
	template_name = "reportes/crear-reporte-obra.html"
	
	def get_queryset(self):
		if not self.request.GET:
			return Obra.objects.none()

		localidad_ids = self.request.GET.getlist("localidad")
		programa_ids = self.request.GET.getlist("programa")
		empresa_ids = self.request.GET.getlist("empresa")
		pctavance = self.request.GET.get("pctavance")
		tipodefiltro = self.request.GET.get("tipodefiltro")
		rubro_ids = self.request.GET.getlist("rubro")

		qs = Obra.objects.all().select_related("obra_empresa", "obra_programa").prefetch_related("obra_localidad_m", "certificado_set")

		if localidad_ids:
			locality_q = Q()
			for l in localidad_ids:
				locality_q |= Q(obra_localidad_m=l)
			qs = qs.filter(locality_q)

		if empresa_ids:
			empresa_q = Q()
			for e in empresa_ids:
				empresa_q |= Q(obra_empresa__id=e)
			qs = qs.filter(empresa_q)

		if programa_ids:
			programa_q = Q()
			for p in programa_ids:
				programa_q |= Q(obra_programa__id=p)
			qs = qs.filter(programa_q)

		if tipodefiltro and pctavance:
			try:
				pct_val = float(pctavance)
				annotated = qs.annotate(pct=Sum(F("certificado__certificado_mes_pct")))
				if tipodefiltro == "1":
					qs = annotated.filter(pct__exact=pct_val)
				elif tipodefiltro == "2":
					qs = annotated.filter(pct__lt=pct_val)
				elif tipodefiltro == "3":
					qs = annotated.filter(pct__gt=pct_val)
			except (ValidationError, ValueError):
				pass

		if rubro_ids and "0" not in rubro_ids:
			rubro_id_list = [int(r) for r in rubro_ids]
			qs = qs.filter(certificado__certificado_rubro_db_id__in=rubro_id_list).distinct()

		financiamiento = self.request.GET.get("financiamiento")
		if financiamiento == "2":
			qs = qs.filter(certificado__certificado_financiamiento="N").distinct()
		elif financiamiento == "3":
			qs = qs.filter(certificado__certificado_financiamiento="P").distinct()
		elif financiamiento == "4":
			qs = qs.filter(certificado__certificado_financiamiento="T").distinct()

		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		for obra in context["object_list"]:
			acum_pesos = 0
			acum_uvi = 0
			certs = obra.certificado_set.all()
			if certs:
				acum_pesos = sum(c.certificado_monto_cobrar or 0 for c in certs)
				acum_uvi = sum(c.certificado_monto_cobrar_uvi or 0 for c in certs)
			setattr(obra, "obra_acum_pesos", acum_pesos)
			setattr(obra, "obra_acum_uvi", acum_uvi)
			saldo = obra.obra_contrato_total_uvi - acum_uvi
			setattr(obra, "saldo_uvi", saldo)
		context["localidades"] = Localidad.objects.all()
		context["empresas"] = Empresa.objects.all()
		context["programas"] = Programa.objects.all()
		return context

@method_decorator(login_required, name="dispatch")
class CrearListaUvi(PermissionRequiredMixin, generic.ListView):
	permission_required = "carga.view_certificado"

	model = Uvi
	title = "Valor UVI"
	context_object_name = "object_list"
	template_name = "reportes/crear-lista-uvi.html"
	
	def get_queryset(self, **kwargs):
		if not self.request.GET:
			fecha_final = datetime.today() + timedelta(days=10)
			fecha_inicial = fecha_final - timedelta(days=60)
			uvi = Uvi.objects.filter(uvi_fecha__range=[fecha_inicial, fecha_final]).order_by("-uvi_fecha")
		else:
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

@login_required
@permission_required('carga.view_certificado', raise_exception=True)
def refresh_uvi_from_bcra(request):
	call_command("bcra_uvi")
	return redirect('/obra/reporte/lista-uvi/')