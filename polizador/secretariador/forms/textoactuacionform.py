from django import forms


class ParrafoForm(forms.Form):
	"""Un considerando editable (parrafo_uno..N)."""
	texto = forms.CharField(label="", widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}))


ParrafoFormSet = forms.formset_factory(ParrafoForm, extra=0)


class ArticuloUnoForm(forms.Form):
	articulo_uno = forms.CharField(label="Artículo 1º", widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}))


class ArticuloDosFilaForm(forms.Form):
	comisionado_id = forms.IntegerField(widget=forms.HiddenInput())
	nombre_cuil = forms.CharField(label="Agente", widget=forms.TextInput(attrs={"class": "form-control"}))
	monto = forms.CharField(label="Monto", widget=forms.TextInput(attrs={"class": "form-control"}))
	subparrafo = forms.CharField(label="Detalle", widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"}))


ArticuloDosFormSet = forms.formset_factory(ArticuloDosFilaForm, extra=0)
