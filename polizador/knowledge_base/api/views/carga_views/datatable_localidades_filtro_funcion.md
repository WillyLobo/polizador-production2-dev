---
symbol: datatable_localidades_filtro_funcion
kind: function
module: api/views/carga_views.py
lines: 691-699
signature_hash: sha1:2e7953d3c07985fb334d8cf1eba59ea4ca69f608
authored: true
---

# datatable_localidades_filtro_funcion

**Módulo:** `api/views/carga_views.py` (líneas 691-699)

## Propósito

Valores distintos (no vacíos) de `localidad_funcion` presentes en la tabla, para poblar el `<select>` de filtro del datatable de Localidades sin hardcodear las opciones.

## Firma

```python
def datatable_localidades_filtro_funcion(request):
```

## Uso real

`GET /v1/api/datatables/localidades/filtro-funcion/`.

## Ver también

- [Localidad](../../../carga/models/Localidad.md)
