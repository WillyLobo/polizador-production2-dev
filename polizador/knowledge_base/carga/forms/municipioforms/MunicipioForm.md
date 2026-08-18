---
symbol: MunicipioForm
kind: class
module: carga/forms/municipioforms.py
lines: 4-20
signature_hash: sha1:cd986c27c93c0368c396d8f077527aad44a2db01
authored: true
---

# MunicipioForm

**Módulo:** `carga/forms/municipioforms.py` (líneas 4-20) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Municipio, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets` (inputs Bootstrap, sin validación más allá de la del modelo). Incluye `id` editable (mismo motivo que `DepartamentoForm`), más `municipio_departamento`/`municipio_region` como selects (no widgets AJAX — catálogos chicos, `<select>` simple alcanza).

## Firma

```python
class MunicipioForm(forms.ModelForm):
```

## Uso real

`CrearMunicipio/UpdateMunicipio` (`carga/views/`), tanto para alta como edición.

## Ver también

- [Municipio](../../models/Municipio.md)
