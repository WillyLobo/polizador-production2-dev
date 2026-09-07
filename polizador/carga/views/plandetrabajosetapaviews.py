from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from carga.models import Certificado, FojaDeMedicion, PlanDeTrabajosEtapa, PlanDeTrabajosEtapaItem, PlanDeTrabajosItem, PlanDeTrabajosRubro
from carga.forms.plandetrabajosetapaforms import build_matriz_form, matriz_field_name
from core.mixins import LogInvalidFormMixin


@method_decorator(login_required, name="dispatch")
class PlanDeTrabajosEtapaMatriz(LogInvalidFormMixin, PermissionRequiredMixin, generic.View):
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

	def _es_readonly(self, rubro):
		"""Los rubros de un Plan de Trabajos que ya no es el vigente (obra reprogramada)
		se muestran de solo lectura: reprogramar es lo que corresponde para seguir
		cargando avance, no reabrir un plan cerrado."""
		return not rubro.rubro_plan.es_vigente()

	def _fojas_predecesoras(self, rubro):
		"""Fojas de toda la cadena de rubros predecesores (si este rubro viene de una
		reprogramación) y cuántas Etapas propias llegó a tener esa cadena. Puede haber más
		Fojas que Etapas: mediciones reales que se siguieron cargando después de que el
		plan viejo dejó de proyectar (el caso que motivó todo esto)."""
		if not rubro.rubro_anterior_id:
			return [], 0
		chain_ids = rubro.rubro_anterior.rubro_cadena_ids()
		fojas = list(FojaDeMedicion.objects.filter(foja_rubro_id__in=chain_ids).order_by("foja_numero"))
		num_etapas = PlanDeTrabajosEtapa.objects.filter(etapa_rubro_id__in=chain_ids).count()
		return fojas, num_etapas

	def _certificados_ya_emitidos(self, rubro):
		"""True si ya se generó algún Certificado vía Foja (Ley 27397) para la cadena
		predecesora. ley27397.resolver_tasas_periodo recalcula el reparto FIFO completo
		desde la primera Foja en cada llamada; completar automáticamente el hueco de
		meses medidos-sin-Etapa DESPUÉS de que eso ya se usó para emitir un Certificado
		podría resolver distinto hacia adelante. Sin Certificados por Foja todavía, no hay
		nada que ese relleno pueda desordenar."""
		if not rubro.rubro_anterior_id:
			return False
		chain_ids = rubro.rubro_anterior.rubro_cadena_ids()
		return Certificado.objects.filter(
			certificado_foja__foja_rubro_id__in=chain_ids, certificado_foja__isnull=False
		).exists()

	def _get_historial_y_gap(self, rubro, existentes):
		"""Separa las Fojas de la cadena predecesora en dos grupos:
		- historial: meses que ya tienen su propia Etapa en el rubro viejo (o que, por algún
		  motivo, no se pueden completar automáticamente) — se muestran de solo lectura.
		- gap: meses medidos por Foja que quedaron sin Etapa en el plan viejo y todavía no
		  se completaron en este rubro — se ofrecen para completar en este mismo submit,
		  precargados con el avance real y bloqueados para edición."""
		fojas, num_etapas = self._fojas_predecesoras(rubro)
		historial_fijo = fojas[:num_etapas]
		posible_gap = fojas[num_etapas:]
		if not posible_gap:
			return historial_fijo, []

		primer_numero_gap = num_etapas + 1
		gap_ya_completado = any(e.etapa_numero == primer_numero_gap for e in existentes)
		if gap_ya_completado:
			return historial_fijo, []
		if self._certificados_ya_emitidos(rubro):
			return historial_fijo + posible_gap, []
		return historial_fijo, posible_gap

	def _historial_value(self, foja, item):
		fojaitem = foja.items.filter(fojaitem_planitem_id__in=item.item_cadena_ids()).first()
		return fojaitem.fojaitem_pct_avance_mes if fojaitem else Decimal("0")

	def _historial_acumulado(self, foja, item):
		fojaitem = foja.items.filter(fojaitem_planitem_id__in=item.item_cadena_ids()).first()
		return fojaitem.fojaitem_pct_acumulado if fojaitem else Decimal("0")

	def _get_anterior_map(self, rubro, items, historial_fojas):
		"""Acumulado ya "consumido" de la incidencia de cada item, a tomar como piso de la
		matriz. Se basa en el avance REAL (Fojas de Medición) y no en lo proyectado por el
		rubro anterior: si un rubro reprogramado usara el acumulado proyectado del plan
		viejo (que llega al 100% de la incidencia en su última etapa, sea cual sea el avance
		real), no quedaría margen para proyectar ninguna etapa nueva.

		Si hay Fojas de historial (columnas de solo lectura, ver _get_historial_y_gap), el
		piso se corta en la última de esas — no en la última Foja de toda la cadena — porque
		los meses posteriores ya están representados como columnas propias de la grilla (el
		hueco recién completado, o etapas ya guardadas): sumarlos dos veces duplicaría el
		acumulado."""
		if historial_fojas:
			ultima = historial_fojas[-1]
			return {item.pk: self._historial_acumulado(ultima, item) for item in items}
		return FojaDeMedicion.anterior_items_map(rubro, items=items)

	def _build_context(self, rubro, items, existentes, form, readonly, historial_fojas, gap_fojas, anterior_map, total_columns):
		num_gap = len(gap_fojas)
		columnas = []
		for col in range(total_columns):
			if col < num_gap:
				foja = gap_fojas[col]
				columnas.append({"numero": None, "fecha": foja.foja_periodo, "gap": True, "foja_numero": foja.foja_numero})
			elif (col - num_gap) < len(existentes):
				etapa = existentes[col - num_gap]
				columnas.append({"numero": etapa.etapa_numero, "fecha": etapa.etapa_fecha, "gap": False})
			else:
				columnas.append({"numero": None, "fecha": None, "gap": False})
		historial_columnas = [
			{"foja_numero": foja.foja_numero, "periodo": foja.foja_periodo}
			for foja in historial_fojas
		]
		rows = [
			{
				"item": item,
				"anterior": anterior_map.get(item.pk, Decimal("0")),
				"historial": [self._historial_value(foja, item) for foja in historial_fojas],
				"cells_columnas": list(zip(
					columnas,
					[form[matriz_field_name(item.pk, col)] for col in range(total_columns)],
				)),
			}
			for item in items
		]
		fixed_colspan = 2 + len(historial_columnas) + (0 if readonly else 1)
		trailing_colspan = 1 if readonly else 2
		return {
			"rubro": rubro,
			"rows": rows,
			"columnas": columnas,
			"historial_columnas": historial_columnas,
			"gap_bloqueado_por_certificados": bool(historial_fojas) and not gap_fojas and self._certificados_ya_emitidos(rubro),
			"fixed_colspan": fixed_colspan,
			"trailing_colspan": trailing_colspan,
			"total_columns": total_columns,
			"form": form,
			"readonly": readonly,
			"rubro_monto_base_pesos": rubro.monto_base_pesos(),
			"rubro_monto_base_uvi": rubro.monto_base_uvi(),
		}

	def get(self, request, pk):
		rubro = self._get_rubro(pk)
		items = self._get_items(rubro)
		existentes = self._get_existentes(rubro)
		readonly = self._es_readonly(rubro)
		historial_fojas, gap_fojas = self._get_historial_y_gap(rubro, existentes)
		anterior_map = self._get_anterior_map(rubro, items, historial_fojas)
		total_columns = max(rubro.rubro_plan.trabajos_meses, len(existentes), len(gap_fojas))

		initial = {}
		for col, foja in enumerate(gap_fojas):
			for item in items:
				initial[matriz_field_name(item.pk, col)] = self._historial_value(foja, item)
		for col, etapa in enumerate(existentes, start=len(gap_fojas)):
			for etapaitem in etapa.items.all():
				initial[matriz_field_name(etapaitem.etapaitem_planitem_id, col)] = etapaitem.etapaitem_pct_proyectado_mes

		form_class = build_matriz_form(items, total_columns, anterior_map)
		form = form_class(initial=initial)
		for col in range(len(gap_fojas)):
			for item in items:
				form.fields[matriz_field_name(item.pk, col)].widget.attrs["readonly"] = True
		if readonly:
			for field in form.fields.values():
				field.widget.attrs["readonly"] = True
		context = self._build_context(rubro, items, existentes, form, readonly, historial_fojas, gap_fojas, anterior_map, total_columns)
		return render(request, self.template_name, context)

	def post(self, request, pk):
		rubro = self._get_rubro(pk)
		if self._es_readonly(rubro):
			return HttpResponseForbidden("Este Plan de Trabajos ya no está vigente: es de solo lectura.")

		items = self._get_items(rubro)
		existentes = self._get_existentes(rubro)
		historial_fojas, gap_fojas = self._get_historial_y_gap(rubro, existentes)
		anterior_map = self._get_anterior_map(rubro, items, historial_fojas)
		total_columns = max(rubro.rubro_plan.trabajos_meses, len(existentes), len(gap_fojas))

		form_class = build_matriz_form(items, total_columns, anterior_map)
		form = form_class(request.POST)

		if form.is_valid():
			with transaction.atomic():
				etapas = list(existentes)
				for col in range(total_columns):
					if col < len(etapas):
						etapa = etapas[col]
					elif col < len(gap_fojas):
						etapa = PlanDeTrabajosEtapa(etapa_rubro=rubro, etapa_fecha=gap_fojas[col].foja_periodo)
						etapa.save()
						etapas.append(etapa)
					else:
						etapa = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)
						etapas.append(etapa)
					for item in items:
						if col < len(gap_fojas):
							valor = self._historial_value(gap_fojas[col], item)
						else:
							valor = form.get_value(item.pk, col)
						etapaitem, _ = PlanDeTrabajosEtapaItem.objects.get_or_create(
							etapaitem_etapa=etapa, etapaitem_planitem=item,
							defaults={"etapaitem_pct_proyectado_mes": valor},
						)
						etapaitem.etapaitem_pct_proyectado_mes = valor
						etapaitem.save()
						if col < len(gap_fojas):
							# El fallback genérico de PlanDeTrabajosEtapaItem.save() calcula el
							# acumulado contra la ÚLTIMA Foja de toda la cadena (pensado para la
							# primera etapa realmente nueva); acá se corrige al acumulado real de
							# ESTA Foja puntual, sin volver a disparar ese cálculo.
							acumulado_real = self._historial_acumulado(gap_fojas[col], item)
							PlanDeTrabajosEtapaItem.objects.filter(pk=etapaitem.pk).update(
								etapaitem_pct_proyectado_acumulado=acumulado_real
							)
			return HttpResponseRedirect(reverse("carga:estado-obra", kwargs={"pk": rubro.rubro_plan.trabajos_obra_id}))

		self._log_form_debug(form)
		context = self._build_context(rubro, items, existentes, form, readonly=False, historial_fojas=historial_fojas, gap_fojas=gap_fojas, anterior_map=anterior_map, total_columns=total_columns)
		return render(request, self.template_name, context)
