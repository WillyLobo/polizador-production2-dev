from django_select2 import forms as s2forms
from django.contrib.auth.mixins import LoginRequiredMixin

from carga.views.ajaxviews import AddRelatedWidgetMixin, SmallCatalogWidgetMixin

class representantetecnicoMultipleWidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "representantetecnico_nombre__icontains",
        "representantetecnico_apellido__icontains",
    ]

class generoagentewidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-generoagente"
    search_fields = ["generoagente_nombre__icontains"]

class tituloprofesionalmultiplewidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
    add_related_url_name = "personalizador:crear-tituloprofesional"
    search_fields = ["tituloprofesional_nombre__icontains"]

class categoriawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-categoria"
    search_fields = ["categoria_nombre__icontains"]

class denominacioncargowidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-denominacioncargo"
    search_fields = ["denominacion__icontains"]

class apartadocargowidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-apartadocargo"
    search_fields = ["apartadocargo_denominacion__icontains"]

class ceicwidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-ceic"
    search_fields = ["ceic__icontains"]

class grupocargowidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-grupocargo"
    search_fields = ["grupo_numero__icontains"]

class actividadespecificawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-actividadespecifica"
    search_fields = ["actividad_especifica_nombre__icontains"]

class directoriowidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-directorio"
    search_fields = ["directorio_nombre__icontains"]

class gerenciawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-gerencia"
    search_fields = ["gerencia_nombre__icontains"]

class direccionwidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-direccion"
    search_fields = ["direccion_nombre__icontains"]

class departamentowidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-departamento"
    search_fields = ["departamento_nombre__icontains"]

class oficinawidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-oficina"
    search_fields = [
        "cargo_directorio__directorio_nombre__icontains",
        "cargo_gerencia__gerencia_nombre__icontains",
        "cargo_direccion__direccion_nombre__icontains",
        "cargo_departamento__departamento_nombre__icontains",
    ]

class agentewidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    """Version propia de personalizador con boton "+"; distinta de
    carga.views.ajaxviews.agentewidget (sin add-related), que sigue usandose tal cual
    en los forms de carga que ya la referencian."""
    add_related_url_name = "personalizador:crear-agente"
    search_fields = [
        "agente_nombres__icontains",
        "agente_apellidos__icontains",
    ]

# --- Widgets dependientes para OficinaForm ---
# Escopean las opciones al nodo del arbol (Directorio > Gerencia > Direccion >
# Departamento) elegido en los campos hermanos mas especificos, y muestran los
# primeros resultados al abrir sin escribir (SmallCatalogWidgetMixin). La consistencia
# real (y la derivacion de los niveles superiores) la garantiza Oficina.clean(); esto
# solo evita que el usuario elija combinaciones sin sentido en el select2.

class OficinaGerenciaDependentWidgetMixin(SmallCatalogWidgetMixin):
    dependent_fields = {"cargo_directorio": "cargo_directorio_actual"}

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        if queryset is None:
            queryset = self.get_queryset()
        directorio_id = dependent_fields.pop("cargo_directorio_actual", None)
        if directorio_id:
            queryset = queryset.filter(gerencia_directorio_id=directorio_id)
        return super().filter_queryset(request, term, queryset)

class oficina_gerenciawidget(OficinaGerenciaDependentWidgetMixin, AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-gerencia"
    search_fields = ["gerencia_nombre__icontains"]

class OficinaDireccionDependentWidgetMixin(SmallCatalogWidgetMixin):
    dependent_fields = {
        "cargo_gerencia": "cargo_gerencia_actual",
        "cargo_directorio": "cargo_directorio_actual",
    }

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        if queryset is None:
            queryset = self.get_queryset()
        gerencia_id = dependent_fields.pop("cargo_gerencia_actual", None)
        directorio_id = dependent_fields.pop("cargo_directorio_actual", None)
        if gerencia_id:
            queryset = queryset.filter(direccion_gerencia_id=gerencia_id)
        elif directorio_id:
            queryset = queryset.filter(direccion_directorio_id=directorio_id)
        return super().filter_queryset(request, term, queryset)

class oficina_direccionwidget(OficinaDireccionDependentWidgetMixin, AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-direccion"
    search_fields = ["direccion_nombre__icontains"]

class OficinaDepartamentoDependentWidgetMixin(SmallCatalogWidgetMixin):
    dependent_fields = {
        "cargo_direccion": "cargo_direccion_actual",
        "cargo_gerencia": "cargo_gerencia_actual",
        "cargo_directorio": "cargo_directorio_actual",
    }

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        if queryset is None:
            queryset = self.get_queryset()
        direccion_id = dependent_fields.pop("cargo_direccion_actual", None)
        gerencia_id = dependent_fields.pop("cargo_gerencia_actual", None)
        directorio_id = dependent_fields.pop("cargo_directorio_actual", None)
        if direccion_id:
            queryset = queryset.filter(departamento_direccion_id=direccion_id)
        elif gerencia_id:
            queryset = queryset.filter(departamento_gerencia_id=gerencia_id)
        elif directorio_id:
            queryset = queryset.filter(departamento_directorio_id=directorio_id)
        return super().filter_queryset(request, term, queryset)

class oficina_departamentowidget(OficinaDepartamentoDependentWidgetMixin, AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
    add_related_url_name = "personalizador:crear-departamento"
    search_fields = ["departamento_nombre__icontains"]
