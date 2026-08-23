---
symbol: select2_rubro_obra
kind: function
module: api/views/select2_views.py
lines: 110-126
signature_hash: sha1:16ec4dafa554cba82365bcf95d4d160e62716621
authored: true
---

# select2_rubro_obra

**Módulo:** `api/views/select2_views.py` (líneas 110-126)

## Propósito

Endpoint de autocompletar sin paginar (límite fijo de 20 resultados) para un `<select>` select2 configurado a mano — mismo formato `{id, text}` que `carga.views.ajaxviews.get_agentes`, no el mecanismo `django-select2`/`ModelSelect2Widget` que usa el resto del sitio. Pese al nombre, busca en `carga.ContratoRubro` (no `CertificadoRubro`/`PlanDeTrabajosRubro`) por `contratorubro_tipo` — el rubro de un documento digital de Contrato, no un rubro de obra en el sentido de plan de trabajos.

## Firma

```python
def select2_rubro_obra(request, q: str=None):
```

## Uso real

`GET /v1/api/select2_rubro_obra/?q=`.

## Ver también

- [ContratoRubro](../../../carga/models/ContratoRubro.md)
