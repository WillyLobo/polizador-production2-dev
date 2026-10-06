---
symbol: datatable_localidades_filtro_funcion
kind: function
module: api/views/carga_views.py
lines: 692-700
signature_hash: sha1:bd699db9bd96b694b71676f963a8bbce6e2fed1b
authored: true
---

# datatable_localidades_filtro_funcion

**Módulo:** `api/views/carga_views.py` (líneas 692-700)

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
