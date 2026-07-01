from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from carga.models import PlanDeTrabajosEtapa, PlanDeTrabajosEtapaItem, PlanDeTrabajosItem, PlanDeTrabajosRubro
from carga.forms.plandetrabajosetapaforms import build_matriz_form, matriz_field_name


@method_decorator(login_required, name="dispatch")
class PlanDeTrabajosEtapaMatriz(PermissionRequiredMixin, generic.View):
	"""Carga/edita de una sola vez todas las Etapas Proyectadas de un Rubro de Plan de
	Trabajos, con una grilla fila=item / columna=etapa (mes), como la planilla de origen."""

	permission_required = ("carga.add_plandetrabajosetapa", "carga.change_plandetrabajosetapa")
	template_name = "plandetrabajosetapa/matriz-plandetrabajosetapa.html"

	def has_permission(self):
		return any(self.request.user.has_perm(perm) for perm in self.get_permission_required())

	def _get_rubro(self, pk):
		return get_object_or_404(PlanDeTrabajosRubro, pk=pk)

	def _get_items(self, rubro):
		return PlanDeTrabajosItem.objects.filter(planitem_rubro=rubro).order_by("planitem_orden")

	def _get_existentes(self, rubro):
		return list(PlanDeTrabajosEtapa.objects.filter(etapa_rubro=rubro).order_by("etapa_numero"))

	def _get_anterior_map(self, rubro, items, existentes):
		"""La matriz edita de una sola vez todas las etapas propias del rubro (existentes
		y nuevas), por lo que el acumulado anterior debe excluirlas: si no, la etapa
		existente más reciente se cuenta dos veces (una via anterior_map, otra como
		columna de la matriz)."""
		exclude_etapa_numero = existentes[0].etapa_numero if existentes else None
		return PlanDeTrabajosEtapa.anterior_items_map(rubro, items=items, exclude_etapa_numero=exclude_etapa_numero)

	def _build_context(self, rubro, items, existentes, anterior_map, form):
		total_columns = max(rubro.rubro_plan.trabajos_meses, len(existentes))
		columnas = [
			{"numero": existentes[col].etapa_numero if col < len(existentes) else None,
			 "fecha": existentes[col].etapa_fecha if col < len(existentes) else None}
			for col in range(total_columns)
		]
		rows = [
			{
				"item": item,
				"anterior": anterior_map.get(item.pk, Decimal("0")),
				"cells": [form[matriz_field_name(item.pk, col)] for col in range(total_columns)],
			}
			for item in items
		]
		return {
			"rubro": rubro,
			"rows": rows,
			"columnas": columnas,
			"total_columns": total_columns,
			"form": form,
			"rubro_monto_base_pesos": rubro.monto_base_pesos(),
			"rubro_monto_base_uvi": rubro.monto_base_uvi(),
		}

	def get(self, request, pk):
		rubro = self._get_rubro(pk)
		items = self._get_items(rubro)
		existentes = self._get_existentes(rubro)
		total_columns = max(rubro.rubro_plan.trabajos_meses, len(existentes))
		anterior_map = self._get_anterior_map(rubro, items, existentes)

		initial = {}
		for col, etapa in enumerate(existentes):
			for etapaitem in etapa.items.all():
				initial[matriz_field_name(etapaitem.etapaitem_planitem_id, col)] = etapaitem.etapaitem_pct_proyectado_mes

		form_class = build_matriz_form(items, total_columns, anterior_map)
		form = form_class(initial=initial)
		return render(request, self.template_name, self._build_context(rubro, items, existentes, anterior_map, form))

	def post(self, request, pk):
		rubro = self._get_rubro(pk)
		items = self._get_items(rubro)
		existentes = self._get_existentes(rubro)
		total_columns = max(rubro.rubro_plan.trabajos_meses, len(existentes))
		anterior_map = self._get_anterior_map(rubro, items, existentes)

		form_class = build_matriz_form(items, total_columns, anterior_map)
		form = form_class(request.POST)

		if form.is_valid():
			with transaction.atomic():
				etapas = list(existentes)
				for col in range(total_columns):
					if col < len(etapas):
						etapa = etapas[col]
					else:
						etapa = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)
						etapas.append(etapa)
					for item in items:
						valor = form.get_value(item.pk, col)
						etapaitem, _ = PlanDeTrabajosEtapaItem.objects.get_or_create(
							etapaitem_etapa=etapa, etapaitem_planitem=item,
							defaults={"etapaitem_pct_proyectado_mes": valor},
						)
						etapaitem.etapaitem_pct_proyectado_mes = valor
						etapaitem.save()
			return HttpResponseRedirect(reverse("carga:estado-obra", kwargs={"pk": rubro.rubro_plan.trabajos_obra_id}))

		return render(request, self.template_name, self._build_context(rubro, items, existentes, anterior_map, form))
