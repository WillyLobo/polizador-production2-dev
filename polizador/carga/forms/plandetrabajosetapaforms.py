from decimal import Decimal
from django import forms


def matriz_field_name(item_pk, col_index):
	return f"item_{item_pk}_col_{col_index}"


def build_matriz_form(items, total_columns, anterior_map):
	"""Devuelve una clase de Form con un campo `item_{pk}_col_{i}` por cada
	combinación (PlanDeTrabajosItem, columna/etapa), para cargar/editar de una
	sola vez todas las etapas proyectadas de un Rubro de Plan de Trabajos."""
	items = list(items)

	class MatrizPlanDeTrabajosEtapaForm(forms.Form):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			for item in items:
				for col in range(total_columns):
					self.fields[matriz_field_name(item.pk, col)] = forms.DecimalField(
						label=item.planitem_nombre,
						max_digits=6,
						decimal_places=3,
						min_value=Decimal("0"),
						max_value=Decimal("100"),
						required=False,
						widget=forms.NumberInput(attrs={
							"class": "form-control form-control-sm text-center matriz-cell",
							"step": "0.001",
						}),
					)

		def get_value(self, item_pk, col_index):
			return self.cleaned_data.get(matriz_field_name(item_pk, col_index)) or Decimal("0")

		def clean(self):
			cleaned_data = super().clean()
			if self.errors:
				return cleaned_data

			for item in items:
				total_item = anterior_map.get(item.pk, Decimal("0"))
				for col in range(total_columns):
					total_item += self.get_value(item.pk, col)
				if total_item > item.planitem_incidencia_pct:
					self.add_error(
						matriz_field_name(item.pk, total_columns - 1),
						f"La suma de todas las etapas de \"{item.planitem_nombre}\" ({total_item}%) "
						f"no puede superar su Incidencia ({item.planitem_incidencia_pct}%)."
					)

			for col in range(total_columns):
				total_col = sum((self.get_value(item.pk, col) for item in items), Decimal("0"))
				if total_col > 100:
					self.add_error(
						None,
						f"La suma de % Proyectado del Mes en la Etapa {col + 1} no puede superar "
						f"100% (actual: {total_col}%)."
					)

			return cleaned_data

	return MatrizPlanDeTrabajosEtapaForm
