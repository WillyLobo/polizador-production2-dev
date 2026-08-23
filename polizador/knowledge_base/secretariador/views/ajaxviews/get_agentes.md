---
symbol: get_agentes
kind: function
module: secretariador/views/ajaxviews.py
lines: 13-16
signature_hash: sha1:381beeb787bc2601ac350608542e3e0a6669653b
authored: true
---

# get_agentes

**Módulo:** `secretariador/views/ajaxviews.py` (líneas 13-16)

## Propósito

Endpoint AJAX de búsqueda de Agentes por nombre completo (`agente_nombreyapellido__icontains`), en formato `{results: [{id, text}]}` — el formato que espera un `<select>` de select2 "a mano" (no un `ModelSelect2Widget` de `django-select2`, que ya trae su propio endpoint genérico). Probablemente un widget más viejo, anterior a la adopción de `django-select2` en este módulo.

## Firma

```python
def get_agentes(request):
```

## Uso real

Consumido por algún campo select2 configurado a mano (fuera del patrón `s2forms.ModelSelect2Widget` del resto del archivo) — buscar `get_agentes` en los templates de `secretariador` para el uso concreto.

## Ver también

_(sin referencias cruzadas)_
